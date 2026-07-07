import os
import uuid
import shutil
import sqlite3
from typing import Optional
from itertools import combinations

import cv2
import numpy as np

from config import (
    DB_PATH,
    CAMERA_ID,
    MODEL_NAME,
    SIMILARITY_THRESHOLD,
    REGISTRATIONS_DIR,
    MIN_DET_SCORE,
    MIN_FACE_AREA,
    MIN_REG_IMAGES,
    BLUR_THRESHOLD,
)
from utils import normalize_embedding, cosine_similarity, get_logger

logger = get_logger(__name__)

def _init_db():

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS faces (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT    NOT NULL,
                embedding BLOB    NOT NULL
            )
        """)

_init_db()

_face_app = None

def get_face_app():

    global _face_app
    if _face_app is None:
        from insightface.app import FaceAnalysis
        logger.info("Loading InsightFace model '%s' …", MODEL_NAME)
        _face_app = FaceAnalysis(name=MODEL_NAME)
        _face_app.prepare(ctx_id=0, det_size=(320, 320))
        logger.info("InsightFace model ready.")
    return _face_app

_embeddings_cache: Optional[tuple] = None

def _invalidate_cache():
    global _embeddings_cache
    _embeddings_cache = None

def get_all_embeddings() -> tuple:

    global _embeddings_cache
    if _embeddings_cache is not None:
        return _embeddings_cache

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT name, embedding FROM faces").fetchall()

    if not rows:
        _embeddings_cache = ([], np.array([]))
        return _embeddings_cache

    from config import EMBEDDING_DIM
    names = []
    embs_list = []
    for r in rows:
        name = r[0]
        blob = r[1]
        arr = np.frombuffer(blob, dtype=np.float32)
        if arr.shape[0] != EMBEDDING_DIM:
            logger.warning(f"Corrupted embedding for '{name}': expected {EMBEDDING_DIM}d, got {arr.shape[0]}d. Skipping.")
            continue
        names.append(name)
        embs_list.append(normalize_embedding(arr))

    if not embs_list:
        _embeddings_cache = ([], np.array([]))
        return _embeddings_cache

    embs_matrix = np.array(embs_list)

    _embeddings_cache = (names, embs_matrix)
    return _embeddings_cache

def get_all_users() -> list:

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT MIN(id), name FROM faces GROUP BY name ORDER BY MIN(id)"
        ).fetchall()

def get_user_count() -> int:

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT COUNT(DISTINCT name) FROM faces").fetchone()[0]

def user_exists(name: str) -> bool:

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT id FROM faces WHERE name = ?", (name,)
        ).fetchone() is not None

def delete_user(user_id: int) -> bool:

    _invalidate_cache()
    with sqlite3.connect(DB_PATH) as conn:

        row = conn.execute(
            "SELECT name FROM faces WHERE id = ?", (user_id,)
        ).fetchone()
        if row is None:
            return False
        name = row[0]
        conn.execute("DELETE FROM faces WHERE name = ?", (name,))

    import shutil, os
    user_image_dir = os.path.join("data", "registrations", name)
    if os.path.exists(user_image_dir):
        shutil.rmtree(user_image_dir)
        logger.info(f"Deleted registration images for user '{name}' from disk.")

    logger.info("Deleted user id=%d name='%s'.", user_id, name)
    return True



def validate_face_image(img_bgr: np.ndarray) -> tuple:

    # 1. Blur Detection (Laplacian Variance)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    if variance < BLUR_THRESHOLD:
        return False, f"Image is blurry (variance: {variance:.1f} < {BLUR_THRESHOLD}). Hold still.", None

    # 2. Face Detection & Validation
    app = get_face_app()
    faces = app.get(img_bgr)
    if not faces:
        return False, "No face detected.", None
    if len(faces) > 1:
        return False, "Multiple faces detected. Use a photo with one face.", None
    f = faces[0]
    if f.det_score < MIN_DET_SCORE:
        return False, f"Detection confidence too low ({f.det_score:.2f}).", None
    area = (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])
    if area < MIN_FACE_AREA:
        return False, "Face is too small. Move closer.", None
    return True, "Valid", f

def register_user(name: str, images: list) -> tuple:

    if not name or not name.strip():
        return False, "Name cannot be empty.", None

    name = name.strip()

    with sqlite3.connect(DB_PATH) as conn:
        existing_count = conn.execute("SELECT COUNT(*) FROM faces WHERE name = ?", (name,)).fetchone()[0]
    if existing_count > 0:
        return False, f"'{name}' is already registered with {existing_count} embeddings. Please delete the existing profile first before re-registering.", None

    if len(images) < MIN_REG_IMAGES:
        return False, (
            f"Please provide at least {MIN_REG_IMAGES} images "
            f"(got {len(images)})."
        ), None

    valid_pairs = []
    for img in images:
        ok, msg, face_obj = validate_face_image(img)
        if not ok:
            return False, f"Image validation failed: {msg}", None
        valid_pairs.append((img, face_obj))

    user_dir = os.path.join(REGISTRATIONS_DIR, name)
    os.makedirs(user_dir, exist_ok=True)
    
    embeddings = []
    for img, face_obj in valid_pairs:
        # Save image to disk (for reference only, no longer read for embeddings)
        path = os.path.join(user_dir, f"{uuid.uuid4().hex}.jpg")
        cv2.imwrite(path, img)
        
        # Use the already extracted embedding directly
        embeddings.append(
            normalize_embedding(face_obj.embedding.astype(np.float32))
        )

    if not embeddings:
        return False, "Failed to extract embeddings from the provided images.", None

    diversity_warning = None
    if len(embeddings) >= 2:
        similarities = []
        for i, j in combinations(range(len(embeddings)), 2):
            sim = float(np.dot(embeddings[i], embeddings[j]))
            similarities.append(sim)
        avg_similarity = sum(similarities) / len(similarities)
        if avg_similarity > 0.97:
            diversity_warning = (
                "⚠️ Registration images are too similar (identical angles/lighting). "
                "For best results, use varied angles and lighting conditions."
            )

    action = "Registered"
    with sqlite3.connect(DB_PATH) as conn:
        for emb in embeddings:
            conn.execute(
                "INSERT INTO faces (name, embedding) VALUES (?, ?)",
                (name, emb.tobytes()),
            )

    _invalidate_cache()
    logger.info(
        "%s user '%s' from %d images.", action, name, len(embeddings)
    )
    return True, f"{action} '{name}' successfully using {len(embeddings)} images.", diversity_warning

def recognize_frame(frame: np.ndarray, threshold: float = SIMILARITY_THRESHOLD) -> tuple:

    app = get_face_app()
    names_list, embs_matrix = get_all_embeddings()
    if embs_matrix is None or len(names_list) == 0 or embs_matrix.shape[0] == 0:
        # No users registered — annotate all detected faces as Unknown and return
        for face in app.get(frame):
            bbox = face.bbox.astype(int)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (128, 128, 128), 2)
            cv2.putText(frame, "Unknown", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 128), 2)
        return frame, []

        from insightface.app import FaceAnalysis
        logger.info("Loading InsightFace model '%s' …", MODEL_NAME)
        _face_app = FaceAnalysis(name=MODEL_NAME)
        _face_app.prepare(ctx_id=0, det_size=(320, 320))
        logger.info("InsightFace model ready.")
    return _face_app

_embeddings_cache: Optional[tuple] = None

def _invalidate_cache():
    global _embeddings_cache
    _embeddings_cache = None

def get_all_embeddings() -> tuple:

    global _embeddings_cache
    if _embeddings_cache is not None:
        return _embeddings_cache

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT name, embedding FROM faces").fetchall()

    if not rows:
        _embeddings_cache = ([], np.array([]))
        return _embeddings_cache

    from config import EMBEDDING_DIM
    names = []
    embs_list = []
    for r in rows:
        name = r[0]
        blob = r[1]
        arr = np.frombuffer(blob, dtype=np.float32)
        if arr.shape[0] != EMBEDDING_DIM:
            logger.warning(f"Corrupted embedding for '{name}': expected {EMBEDDING_DIM}d, got {arr.shape[0]}d. Skipping.")
            continue
        names.append(name)
        embs_list.append(normalize_embedding(arr))

    if not embs_list:
        _embeddings_cache = ([], np.array([]))
        return _embeddings_cache

    embs_matrix = np.array(embs_list)

    _embeddings_cache = (names, embs_matrix)
    return _embeddings_cache

def get_all_users() -> list:

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT MIN(id), name FROM faces GROUP BY name ORDER BY MIN(id)"
        ).fetchall()

def get_user_count() -> int:

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT COUNT(DISTINCT name) FROM faces").fetchone()[0]

def user_exists(name: str) -> bool:

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT id FROM faces WHERE name = ?", (name,)
        ).fetchone() is not None

def delete_user(user_id: int) -> bool:

    _invalidate_cache()
    with sqlite3.connect(DB_PATH) as conn:

        row = conn.execute(
            "SELECT name FROM faces WHERE id = ?", (user_id,)
        ).fetchone()
        if row is None:
            return False
        name = row[0]
        conn.execute("DELETE FROM faces WHERE name = ?", (name,))

    import shutil, os
    user_image_dir = os.path.join("data", "registrations", name)
    if os.path.exists(user_image_dir):
        shutil.rmtree(user_image_dir)
        logger.info(f"Deleted registration images for user '{name}' from disk.")

    logger.info("Deleted user id=%d name='%s'.", user_id, name)
    return True



def validate_face_image(img_bgr: np.ndarray) -> tuple:

    # 1. Blur Detection (Laplacian Variance)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    if variance < BLUR_THRESHOLD:
        return False, f"Image is blurry (variance: {variance:.1f} < {BLUR_THRESHOLD}). Hold still.", None

    # 2. Face Detection & Validation
    app = get_face_app()
    faces = app.get(img_bgr)
    if not faces:
        return False, "No face detected.", None
    if len(faces) > 1:
        return False, "Multiple faces detected. Use a photo with one face.", None
    f = faces[0]
    if f.det_score < MIN_DET_SCORE:
        return False, f"Detection confidence too low ({f.det_score:.2f}).", None
    area = (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])
    if area < MIN_FACE_AREA:
        return False, "Face is too small. Move closer.", None
    return True, "Valid", f

def register_user(name: str, images: list) -> tuple:

    if not name or not name.strip():
        return False, "Name cannot be empty.", None

    name = name.strip()

    with sqlite3.connect(DB_PATH) as conn:
        existing_count = conn.execute("SELECT COUNT(*) FROM faces WHERE name = ?", (name,)).fetchone()[0]
    if existing_count > 0:
        return False, f"'{name}' is already registered with {existing_count} embeddings. Please delete the existing profile first before re-registering.", None

    if len(images) < MIN_REG_IMAGES:
        return False, (
            f"Please provide at least {MIN_REG_IMAGES} images "
            f"(got {len(images)})."
        ), None

    valid_pairs = []
    for img in images:
        ok, msg, face_obj = validate_face_image(img)
        if not ok:
            return False, f"Image validation failed: {msg}", None
        valid_pairs.append((img, face_obj))

    user_dir = os.path.join(REGISTRATIONS_DIR, name)
    os.makedirs(user_dir, exist_ok=True)
    
    embeddings = []
    for img, face_obj in valid_pairs:
        # Save image to disk (for reference only, no longer read for embeddings)
        path = os.path.join(user_dir, f"{uuid.uuid4().hex}.jpg")
        cv2.imwrite(path, img)
        
        # Use the already extracted embedding directly
        embeddings.append(
            normalize_embedding(face_obj.embedding.astype(np.float32))
        )

    if not embeddings:
        return False, "Failed to extract embeddings from the provided images.", None

    diversity_warning = None
    if len(embeddings) >= 2:
        similarities = []
        for i, j in combinations(range(len(embeddings)), 2):
            sim = float(np.dot(embeddings[i], embeddings[j]))
            similarities.append(sim)
        avg_similarity = sum(similarities) / len(similarities)
        if avg_similarity > 0.97:
            diversity_warning = (
                "⚠️ Registration images are too similar (identical angles/lighting). "
                "For best results, use varied angles and lighting conditions."
            )

    action = "Registered"
    with sqlite3.connect(DB_PATH) as conn:
        for emb in embeddings:
            conn.execute(
                "INSERT INTO faces (name, embedding) VALUES (?, ?)",
                (name, emb.tobytes()),
            )

    _invalidate_cache()
    logger.info(
        "%s user '%s' from %d images.", action, name, len(embeddings)
    )
    return True, f"{action} '{name}' successfully using {len(embeddings)} images.", diversity_warning

def recognize_frame(frame: np.ndarray, threshold: float = SIMILARITY_THRESHOLD) -> tuple:

    app = get_face_app()
    names_list, embs_matrix = get_all_embeddings()
    if embs_matrix is None or len(names_list) == 0 or embs_matrix.shape[0] == 0:
        # No users registered — annotate all detected faces as Unknown and return
        for face in app.get(frame):
            bbox = face.bbox.astype(int)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (128, 128, 128), 2)
            cv2.putText(frame, "Unknown", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 128), 2)
        return frame, []

    detected = app.get(frame)
    results = []

    for face in detected:
        bbox      = face.bbox.astype(int)
        query_emb = normalize_embedding(face.embedding.astype(np.float32))

        best_name = "Unknown"
        best_sim  = 0.0

        if len(names_list) > 0:
            sims      = np.dot(embs_matrix, query_emb) * 100
            best_idx  = int(np.argmax(sims))
            best_sim  = float(sims[best_idx])
            best_name = names_list[best_idx]

        recognized = best_sim >= threshold
        if not recognized:
            best_name = "Unknown"

        results.append({
            "name":       best_name,
            "similarity": round(best_sim, 2),
            "bbox":       bbox.tolist(),
            "recognized": recognized,
        })

        # Premium Colors: Mint Green vs Amber/Orange (BGR)
        color = (138, 255, 126) if recognized else (0, 165, 255)
        label = f"{best_name}  {best_sim:.1f}%"

        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
        
        # 1. Corner-Only Bounding Boxes
        length = int(max(20, min(x2 - x1, y2 - y1) * 0.2))
        thickness = 2
        # Top-left
        cv2.line(frame, (x1, y1), (x1 + length, y1), color, thickness)
        cv2.line(frame, (x1, y1), (x1, y1 + length), color, thickness)
        # Top-right
        cv2.line(frame, (x2, y1), (x2 - length, y1), color, thickness)
        cv2.line(frame, (x2, y1), (x2, y1 + length), color, thickness)
        # Bottom-left
        cv2.line(frame, (x1, y2), (x1 + length, y2), color, thickness)
        cv2.line(frame, (x1, y2), (x1, y2 - length), color, thickness)
        # Bottom-right
        cv2.line(frame, (x2, y2), (x2 - length, y2), color, thickness)
        cv2.line(frame, (x2, y2), (x2, y2 - length), color, thickness)

        # 2. Translucent Text Background
        (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        
        bg_x1, bg_y1 = max(0, x1), max(0, y1 - lh - 14)
        bg_x2, bg_y2 = min(frame.shape[1], x1 + lw + 10), min(frame.shape[0], y1)
        
        # Alpha blend via ROI
        if bg_y1 < bg_y2 and bg_x1 < bg_x2:
            roi = frame[bg_y1:bg_y2, bg_x1:bg_x2]
            overlay_roi = roi.copy()
            cv2.rectangle(overlay_roi, (0, 0), (bg_x2 - bg_x1, bg_y2 - bg_y1), color, -1)
            cv2.addWeighted(overlay_roi, 0.35, roi, 0.65, 0, roi)

        cv2.putText(
            frame, label,
            (bg_x1 + 5, bg_y2 - 7),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2,
        )

    return frame, results

_camera_cap: Optional[cv2.VideoCapture] = None

def open_camera() -> bool:

    global _camera_cap
    if _camera_cap is not None and _camera_cap.isOpened():
        return True
    _camera_cap = cv2.VideoCapture(CAMERA_ID)
    return _camera_cap.isOpened()

def release_camera():

    global _camera_cap
    if _camera_cap is not None:
        _camera_cap.release()
        _camera_cap = None

def capture_frame() -> Optional[np.ndarray]:

    global _camera_cap
    if _camera_cap is None or not _camera_cap.isOpened():
        if not open_camera():
            return None
    ret, frame = _camera_cap.read()
    return frame if ret else None

def is_camera_available() -> bool:

    global _camera_cap
    if _camera_cap is not None and _camera_cap.isOpened():
        return True
    cap = cv2.VideoCapture(CAMERA_ID)
    result = cap.isOpened()
    cap.release()
    return result
