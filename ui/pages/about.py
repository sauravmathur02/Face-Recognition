import streamlit as st
from ui.components import render_header

def render():
    render_header("About", "System Architecture & Documentation")

    st.markdown("""
    <div style="max-width: 700px; margin-bottom: 3rem;">
        <div style="font-size:1.25rem; font-weight:500; color:#F8FAFC; line-height:1.6; margin-bottom:1rem;">
            Vision AI is a low-latency, real-time face recognition platform utilizing state-of-the-art computer vision models.
        </div>
        <div style="font-size:0.9rem; color:#94A3B8; line-height:1.6;">
            The system registers human faces by aggregating high-dimensional embeddings and leverages vectorized cosine distance to perform instantaneous identity verification against a local SQLite repository.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">Inference Pipeline</div>', unsafe_allow_html=True)
    
    steps = [
        ("ph-video-camera", "Data Acquisition", "OpenCV retrieves a continuous BGR frame buffer from the primary video device."),
        ("ph-corners-out", "Face Localization", "InsightFace (buffalo_l) detects facial bounding boxes and 5-point landmarks."),
        ("ph-vector-three", "Feature Extraction", "Generates a 512-dimensional float32 vector representation of the detected face."),
        ("ph-arrows-in", "Normalization", "Applies L2 normalization to the embedding vector for accurate distance calculation."),
        ("ph-corners-out", "Face Localization", "InsightFace (buffalo_sc) detects facial bounding boxes and 5-point landmarks."),
        ("ph-fingerprint", "Feature Extraction", "The model projects faces into a high-dimensional 512-d embedding space."),
        ("ph-math-operations", "Vector Normalization", "Embeddings are L2-normalized to project them onto a unit hypersphere."),
        ("ph-crosshair", "Similarity Search", "Real-time vectorized cosine similarity matches the anchor against all stored profiles.")
    ]

    for icon, title, desc in steps:
        st.markdown(f"""
        <div class="premium-card" style="margin-bottom:0.75rem; padding:1.25rem; display:flex; align-items:center; gap:1.25rem;">
            <div style="width:48px; height:48px; border-radius:12px; background:linear-gradient(135deg, #1A1A1A, #111111); border:1px solid #222222; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <i class="ph {icon}" style="font-size:1.5rem; color:#F8FAFC;"></i>
            </div>
            <div>
                <div style="font-size:0.95rem; font-weight:600; color:#F8FAFC; margin-bottom:0.25rem;">{title}</div>
                <div style="font-size:0.875rem; color:#94A3B8; line-height:1.5;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr style="margin:2.5rem 0;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">Tech Stack</div>', unsafe_allow_html=True)
    
    tags = [
        "InsightFace", "buffalo_sc", "SQLite", "OpenCV", "NumPy", "Streamlit", "Python 3.10+"
    ]
    
    tags_html = "".join([f'<div class="badge" style="margin-right:0.5rem; margin-bottom:0.5rem;">{t}</div>' for t in tags])
    st.markdown(f'<div style="display:flex; flex-wrap:wrap;">{tags_html}</div>', unsafe_allow_html=True)
