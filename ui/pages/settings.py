import os
import streamlit as st
from config import MODEL_NAME, SIMILARITY_THRESHOLD, DB_PATH, CAMERA_ID

def render():
    st.markdown("""
    <div class="page-title">Settings</div>
    <div class="page-subtitle">System configuration — read only</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        display:inline-flex; align-items:center; gap:0.5rem;
        padding:0.35rem 0.85rem;
        background:rgba(245,158,11,0.1);
        border:1px solid rgba(245,158,11,0.3);
        border-radius:20px;
        font-size:0.78rem; color:#FCD34D; font-weight:600;
        margin-bottom:1.5rem;
    ">
        🔒 Read-only — edit config.py to change these values
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="margin-bottom:1rem;">
        <div style="font-size:0.72rem; font-weight:700; color:#64748B;
                    text-transform:uppercase; letter-spacing:0.1em;
                    margin-bottom:1rem;">Recognition</div>
    """, unsafe_allow_html=True)

    _setting_row("🧠", "AI Model",             MODEL_NAME,
                 "Face detection + embedding extraction")
    _setting_row("🎯", "Similarity Threshold", f"{SIMILARITY_THRESHOLD}%",
                 "Cosine similarity required to identify a face")
    _setting_row("📐", "Embedding Dimensions", "512",
                 "InsightFace buffalo_l output vector size")
    _setting_row("📏", "Detection Size",       "320 × 320 px",
                 "Input resolution for face detection")

    st.markdown("</div>", unsafe_allow_html=True)

    abs_db = os.path.abspath(DB_PATH)
    st.markdown("""
    <div class="glass-card" style="margin-bottom:1rem;">
        <div style="font-size:0.72rem; font-weight:700; color:#64748B;
                    text-transform:uppercase; letter-spacing:0.1em;
                    margin-bottom:1rem;">Database</div>
    """, unsafe_allow_html=True)

    _setting_row("🗄️", "Engine",    "SQLite",   "Embedded, zero-configuration database")
    _setting_row("📄", "File",      DB_PATH,    abs_db)
    _setting_row("📋", "Table",     "faces",    "id · name · embedding (BLOB)")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div style="font-size:0.72rem; font-weight:700; color:#64748B;
                    text-transform:uppercase; letter-spacing:0.1em;
                    margin-bottom:1rem;">Camera</div>
    """, unsafe_allow_html=True)

    _setting_row("📹", "Camera Device ID", str(CAMERA_ID),
                 "OpenCV VideoCapture index")
    _setting_row("⚡", "Target FPS",       "~25",
                 "Approximate recognition frame rate")

    st.markdown("</div>", unsafe_allow_html=True)

def _setting_row(icon: str, label: str, value: str, hint: str = ""):

    hint_html = (
        f'<div style="font-size:0.72rem; color:#334155; margin-top:0.15rem;">{hint}</div>'
        if hint else ""
    )
    st.markdown(f"""
    <div class="setting-row">
        <div>
            <div class="setting-label">{icon} {label}</div>
            {hint_html}
        </div>
        <div class="setting-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)
