# Vision AI: Face Recognition System

## Project Description
**Vision AI** is a high-performance, production-grade Face Recognition System designed to mimic commercial security pipelines. It is built to seamlessly register and identify human faces in real-time using a decoupled architecture. The backend leverages a blazing-fast **FastAPI** server powered by **InsightFace's MobileFaceNet (`buffalo_sc`)** model for highly optimized CPU edge-inference. For persistence, it utilizes a lightweight **SQLite** database to store mathematically robust 512-dimensional L2-normalized embeddings, guaranteeing lightning-fast lookup via Cosine Similarity. 

The presentation layer is a modern **React (Vite)** Single Page Application featuring a cinematic, Palantir-inspired dark UI. The frontend includes a smart 1:1 face detection HUD, real-time webcam processing, and glassmorphic aesthetic dashboards for identity management and system monitoring. Whether scanning live camera feeds or managing identity enrollments, the system provides instantaneous feedback and high accuracy (≥89% similarity threshold).

---

## Features

| Area | Description |
|------|-------------|
| **Architecture** | Fully decoupled Backend (Python/FastAPI) and Frontend (React/Vite) |
| **Registration** | Upload images or capture directly via webcam with a smart 1:1 face detection HUD |
| **Recognition** | Live high-fps webcam inference returning accurate bounding boxes, identities, and confidence scores |
| **Database** | Lightweight SQLite (`faces.db`) storing 512-dimensional embeddings for robust multi-angle matching |
| **Dashboard** | View registered identities, monitor system health, and manage API configurations |

---

## Tech Stack

| Component | Detail |
|-----------|--------|
| **AI Model** | InsightFace `buffalo_sc` (MobileFaceNet) — optimized for CPU edge-inference |
| **Backend** | Python, FastAPI, Uvicorn, OpenCV |
| **Frontend** | React, Vite, Vanilla CSS (Glassmorphism UI) |
| **Matching** | Cosine similarity (L2-normalized dot product) |
| **Thresholds** | **89%** similarity |
| **Database** | SQLite (`faces.db`) |

---

## Setup & Running

This project uses a decoupled architecture. You need to run the **Backend** and the **Frontend** in two separate terminals.

### 1. Start the FastAPI Backend
```bash
# Open Terminal 1
cd "Face Recognition"

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
python -m uvicorn api.main:app --reload
```
> **Note:** First launch downloads the `buffalo_sc` model weights automatically into `~/.insightface/models/` — one time only.

### 2. Start the React Frontend
```bash
# Open Terminal 2
cd "Face Recognition/frontend"

# Install Node modules (first time only)
npm install

# Start the Vite development server
npm run dev
```

---

## Project Structure

```
Face Recognition/
├── api/
│   └── main.py         ← FastAPI REST endpoints (/api/recognize, /api/register)
├── frontend/           ← React SPA (Vite)
│   ├── src/
│   │   ├── index.css   ← Global Design System & Animations
│   │   ├── api/        ← Axios API client
│   │   ├── components/ ← Reusable UI components
│   │   └── pages/      ← Routes: Recognition, Register, Identities
├── backend.py          ← Core AI engine (InsightFace + SQLite + Cosine Similarity)
├── config.py           ← System constants (thresholds, DB path, model config)
├── utils.py            ← Math and logging utilities
├── requirements.txt    ← Python dependencies
└── faces.db            ← SQLite Database (auto-generated)
```

---

## How the AI Pipeline Works

```
Webcam Frame (Frontend)
    ↓
Sent via multipart/form-data to FastAPI (/api/recognize)
    ↓
InsightFace (buffalo_sc) — Detects face, extracts 512-D embedding
    ↓
L2 Normalize embedding
    ↓
Cosine Similarity  vs.  all stored embeddings (vectorized dot product)
    ↓
SQLite lookup  —  Matches WHERE similarity ≥ 89%
    ↓
Returns JSON: Bounding Boxes + Name + Similarity % (or Unknown)
```
