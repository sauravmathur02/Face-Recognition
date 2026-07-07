import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base64
import time
import numpy as np
import cv2
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import backend as engine
from config import (
    MODEL_NAME, SIMILARITY_THRESHOLD, DB_PATH,
    CAMERA_ID, MIN_FACE_AREA, MIN_DET_SCORE,
    MIN_REG_IMAGES, BLUR_THRESHOLD, EMBEDDING_DIM
)

app = FastAPI(title="Vision AI — Face Recognition API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecognizeRequest(BaseModel):
    frame: str  # base64 encoded JPEG

class ThresholdRequest(BaseModel):
    threshold: int

_runtime_threshold = SIMILARITY_THRESHOLD

@app.get("/api/health")
def health():
    return {
        "status": "online",
        "model": MODEL_NAME,
        "threshold": _runtime_threshold,
        "db": DB_PATH
    }

@app.get("/api/config")
def get_config():
    return {
        "model_name": MODEL_NAME,
        "similarity_threshold": _runtime_threshold,
        "embedding_dim": EMBEDDING_DIM,
        "min_face_area": MIN_FACE_AREA,
        "min_det_score": MIN_DET_SCORE,
        "min_reg_images": MIN_REG_IMAGES,
        "blur_threshold": BLUR_THRESHOLD,
        "camera_id": CAMERA_ID,
        "db_path": DB_PATH,
    }

@app.post("/api/threshold")
def update_threshold(body: ThresholdRequest):
    global _runtime_threshold
    _runtime_threshold = body.threshold
    return {"threshold": _runtime_threshold}

@app.get("/api/users")
def list_users():
    rows = engine.get_all_users()
    users = []
    for idx, (uid, uname) in enumerate(rows, start=1):
        import sqlite3
        with sqlite3.connect(DB_PATH) as conn:
            emb_count = conn.execute(
                "SELECT COUNT(*) FROM faces WHERE name = ?", (uname,)
            ).fetchone()[0]
        users.append({
            "id": uid,
            "display_id": f"{idx:04d}",
            "name": uname,
            "embedding_count": emb_count
        })
    return {"users": users, "total": len(users)}

@app.get("/api/users/count")
def user_count():
    return {"count": engine.get_user_count()}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    ok = engine.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "message": "Identity revoked successfully"}

@app.post("/api/register")
async def register_user(
    name: str = Form(...),
    files: list[UploadFile] = File(...)
):
    images = []
    for f in files:
        data = await f.read()
        arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is not None:
            images.append(img)

    if not images:
        raise HTTPException(status_code=400, detail="No valid images provided")

    ok, msg, warning = engine.register_user(name.strip(), images)
    return {
        "success": ok,
        "message": msg,
        "warning": warning
    }

@app.post("/api/recognize")
async def recognize(body: RecognizeRequest):
    t0 = time.time()
    try:
        img_bytes = base64.b64decode(body.frame)
        arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image data")
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to decode frame")

    _, results = engine.recognize_frame(frame, threshold=_runtime_threshold)
    latency_ms = round((time.time() - t0) * 1000, 1)

    return {
        "results": results,
        "latency_ms": latency_ms,
        "threshold": _runtime_threshold,
        "frame_count": len(results)
    }

@app.get("/api/stats")
def get_stats():
    import sqlite3
    with sqlite3.connect(DB_PATH) as conn:
        total_users = conn.execute("SELECT COUNT(DISTINCT name) FROM faces").fetchone()[0]
        total_embeddings = conn.execute("SELECT COUNT(*) FROM faces").fetchone()[0]
    db_size_kb = round(os.path.getsize(DB_PATH) / 1024, 1) if os.path.exists(DB_PATH) else 0
    avg_embeddings = round(total_embeddings / total_users, 1) if total_users > 0 else 0
    return {
        "total_users": total_users,
        "total_embeddings": total_embeddings,
        "avg_embeddings_per_user": avg_embeddings,
        "db_size_kb": db_size_kb,
        "model": MODEL_NAME,
        "threshold": _runtime_threshold
    }

# Serve React frontend for production
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        return FileResponse(os.path.join(frontend_dist, "index.html"))
