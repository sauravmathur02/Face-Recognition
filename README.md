# Face Recognition

A clean, minimal face recognition pipeline built as an interview assignment.

---

## Features

| Page | Description |
|------|-------------|
| **Home** | Landing page — tech stack overview, quick-start buttons |
| **Register User** | Upload images or capture from webcam → stores average embedding in SQLite |
| **Face Recognition** | Live webcam feed with bounding boxes, name, and similarity % |
| **Registered Users** | Table — ID, name, delete button, search box |
| **Settings** | Read-only config display |
| **About** | Workflow explanation |

---

## Tech Stack

| Component | Detail |
|-----------|--------|
| AI Model | InsightFace `buffalo_l` — detection + 512-d embedding |
| Similarity | Cosine similarity (L2-normalized dot product) |
| Threshold | **89%** |
| Database | SQLite (`faces.db`) |
| UI | Streamlit |
| Language | Python 3.9+ |

---

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

> **First launch** downloads the `buffalo_l` model weights (~500 MB) automatically into `~/.insightface/models/` — one time only.

---

## Project Structure

```
Face/
├── app.py              ← Streamlit entry point, sidebar, routing
├── backend.py          ← InsightFace + SQLite + cosine similarity (no UI)
├── config.py           ← All constants: threshold, model, DB path, camera
├── utils.py            ← normalize_embedding, cosine_similarity, logger
├── requirements.txt
├── README.md
└── ui/
    ├── styles.py       ← Global dark glassmorphism CSS
    └── pages/
        ├── home.py         ← Landing page
        ├── register.py     ← Register user (upload or webcam)
        ├── recognition.py  ← Live webcam recognition
        ├── users.py        ← Registered users table
        ├── settings.py     ← Read-only settings
        └── about.py        ← Workflow explanation
```

---

## How It Works

```
Webcam Frame
    ↓
InsightFace (buffalo_l)  —  detect face, extract 512-d embedding
    ↓
L2 Normalize embedding
    ↓
Cosine Similarity  vs.  all stored embeddings (vectorized dot product)
    ↓
SQLite lookup  —  name WHERE similarity ≥ 89%
    ↓
✅ Name + Similarity%   OR   ❓ Unknown
```

---

## Database Schema

```sql
CREATE TABLE faces (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT    NOT NULL,
    embedding BLOB    NOT NULL
);
```

---

## Configuration (`config.py`)

| Constant | Value | Description |
|----------|-------|-------------|
| `DB_PATH` | `faces.db` | SQLite database file |
| `MODEL_NAME` | `buffalo_l` | InsightFace model |
| `SIMILARITY_THRESHOLD` | `89` | Minimum cosine similarity (%) to recognize |
| `MIN_FACE_AREA` | `4000` | Minimum face area in pixels² |
| `MIN_DET_SCORE` | `0.60` | Minimum InsightFace detection confidence |
| `MIN_REG_IMAGES` | `3` | Minimum images required to register a user |
| `CAMERA_ID` | `0` | OpenCV camera device index |
