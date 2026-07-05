import os
import streamlit as st
from config import MODEL_NAME, SIMILARITY_THRESHOLD, DB_PATH, CAMERA_ID
from ui.components import render_header

def render():
    render_header("Settings", "System Configuration")

    st.markdown("""
    <div style="display:inline-flex; align-items:center; gap:0.5rem; padding:0.5rem 0.875rem; background-color:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.2); border-radius:6px; font-size:0.875rem; color:#F59E0B; margin-bottom:2rem;">
        <i class="ph-fill ph-lock-key"></i> Configuration is locked. Modify config.py to apply changes.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">Inference Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="premium-card" style="margin-bottom:2rem; padding:0;">', unsafe_allow_html=True)
    _setting_row("ph-brain", "Model Architecture", MODEL_NAME, "Detection and feature extraction")
    _setting_row("ph-target", "Confidence Threshold", f"{SIMILARITY_THRESHOLD}%", "Minimum cosine similarity required")
    _setting_row("ph-vector-three", "Feature Vector", "512-d", "Dimensionality of generated embeddings")
    _setting_row("ph-bounding-box", "Input Resolution", "320x320", "Normalized face crop dimension", last=True)
    st.markdown('</div>', unsafe_allow_html=True)

    abs_db = os.path.abspath(DB_PATH)
    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">Storage</div>', unsafe_allow_html=True)
    st.markdown('<div class="premium-card" style="margin-bottom:2rem; padding:0;">', unsafe_allow_html=True)
    _setting_row("ph-database", "Database Engine", "SQLite", "Local persistent storage")
    _setting_row("ph-file-sql", "Path", DB_PATH, abs_db)
    _setting_row("ph-table", "Schema", "faces", "id, name, embedding (blob)", last=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">Hardware Integration</div>', unsafe_allow_html=True)
    st.markdown('<div class="premium-card" style="padding:0;">', unsafe_allow_html=True)
    _setting_row("ph-webcam", "Camera Interface", str(CAMERA_ID), "OpenCV device index")
    _setting_row("ph-lightning", "Target Framerate", "~25 FPS", "Expected real-time processing speed", last=True)
    st.markdown('</div>', unsafe_allow_html=True)

def _setting_row(icon: str, label: str, value: str, hint: str = "", last: bool = False):
    border_bottom = "border-bottom:1px solid #1A1A1A;" if not last else ""
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; padding:1.25rem 1.5rem; {border_bottom}">
        <div style="display:flex; align-items:flex-start; gap:1rem;">
            <i class="ph {icon}" style="font-size:1.25rem; color:#64748B; margin-top:0.1rem;"></i>
            <div>
                <div style="font-size:0.875rem; font-weight:500; color:#E2E8F0; margin-bottom:0.15rem;">{label}</div>
                <div style="font-size:0.75rem; color:#64748B;">{hint}</div>
            </div>
        </div>
        <div style="font-size:0.875rem; font-weight:600; color:#F8FAFC; font-family:monospace;">{value}</div>
    </div>
    """, unsafe_allow_html=True)
