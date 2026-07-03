import os
import glob
import uuid
import shutil
import sqlite3
from typing import Optional

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

    names = [r[0] for r in rows]
    embs  = np.array([
        normalize_embedding(np.frombuffer(r[1], dtype=np.float32))
        for r in rows
    ])
    _embeddings_cache = (names, embs)
    return _embeddings_cache

def get_all_users() -> list:

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT id, name FROM faces ORDER BY id"
        ).fetchall()

def get_user_count() -> int:

    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT COUNT(*) FROM faces").fetchone()[0]

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
        conn.execute("DELETE FROM faces WHERE id = ?", (user_id,))

    user_dir = os.path.join(REGISTRATIONS_DIR, name)
    shutil.rmtree(user_dir, ignore_errors=True)
    logger.info("Deleted user id=%d name='%s'.", user_id, name)
    return True

def _get_registration_images(name: str) -> list:
    user_dir = os.path.join(REGISTRATIONS_DIR, name)
    if not os.path.exists(user_dir):
        return []
    return (
        glob.glob(os.path.join(user_dir, "*.jpg"))
        + glob.glob(os.path.join(user_dir, "*.png"))
    )

def validate_face_image(img_bgr: np.ndarray) -> tuple:

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
        return False, "Face is too small or blurry. Move closer.", None
    return True, "Valid", f

def register_user(name: str, images: list) -> tuple:

    if not name or not name.strip():
        return False, "Name cannot be empty."

    name = name.strip()

    if len(images) < MIN_REG_IMAGES:
        return False, (
            f"Please provide at least {MIN_REG_IMAGES} images "
            f"(got {len(images)})."
        )

    valid_pairs = []
    for img in images:
        ok, msg, face_obj = validate_face_image(img)
        if not ok:
            return False, f"Image validation failed: {msg}"
        valid_pairs.append((img, face_obj))

    user_dir = os.path.join(REGISTRATIONS_DIR, name)
    os.makedirs(user_dir, exist_ok=True)
    for img, _ in valid_pairs:
        path = os.path.join(user_dir, f"{uuid.uuid4().hex}.jpg")
        cv2.imwrite(path, img)

    app = get_face_app()
    embeddings = []
    for img_path in _get_registration_images(name):
        img = cv2.imread(img_path)
        if img is None:
            continue
        faces = app.get(img)
        valid_faces = [
            f for f in faces
            if f.det_score >= MIN_DET_SCORE
            and (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]) >= MIN_FACE_AREA
        ]
        if valid_faces:
            best = max(
                valid_faces,
                key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]),
            )
            embeddings.append(
                normalize_embedding(best.embedding.astype(np.float32))
            )

    if not embeddings:
        return False, "Failed to extract embeddings from the provided images."

    avg_emb = normalize_embedding(
        np.mean(embeddings, axis=0).astype(np.float32)
    )

    with sqlite3.connect(DB_PATH) as conn:
        existing = conn.execute(
            "SELECT id FROM faces WHERE name = ?", (name,)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE faces SET embedding = ? WHERE name = ?",
                (avg_emb.tobytes(), name),
            )
            action = "Updated"
        else:
            conn.execute(
                "INSERT INTO faces (name, embedding) VALUES (?, ?)",
                (name, avg_emb.tobytes()),
            )
            action = "Registered"

    _invalidate_cache()
    logger.info(
        "%s user '%s' from %d images.", action, name, len(embeddings)
    )
    return True, f"{action} '{name}' successfully using {len(embeddings)} images."

def recognize_frame(frame: np.ndarray) -> tuple:

    app = get_face_app()
    names_list, embs_matrix = get_all_embeddings()
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

        recognized = best_sim >= SIMILARITY_THRESHOLD
        if not recognized:
            best_name = "Unknown"

        results.append({
            "name":       best_name,
            "similarity": round(best_sim, 2),
            "bbox":       bbox.tolist(),
            "recognized": recognized,
        })

        color = (34, 197, 94) if recognized else (239, 68, 68)
        label = f"{best_name}  {best_sim:.1f}%"

        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)

        (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(
            frame,
            (bbox[0], bbox[1] - lh - 14),
            (bbox[0] + lw + 10, bbox[1]),
            color, -1,
        )
        cv2.putText(
            frame, label,
            (bbox[0] + 5, bbox[1] - 7),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2,
        )

    return frame, results

_camera_cap: Optional[cv2.VideoCapture] = None
_camera_available_cache: Optional[bool] = None

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

    global _camera_cap, _camera_available_cache
    if _camera_cap is not None and _camera_cap.isOpened():
        return True
    if _camera_available_cache is not None:
        return _camera_available_cache
    cap = cv2.VideoCapture(CAMERA_ID)
    _camera_available_cache = cap.isOpened()
    cap.release()
    return _camera_available_cache
