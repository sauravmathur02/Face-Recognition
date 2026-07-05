import streamlit as st
import backend as api
from config import MODEL_NAME, SIMILARITY_THRESHOLD, DB_PATH, CAMERA_ID
from ui.components import render_header

def render():
    render_header("Overview", "Vision AI Face Recognition Engine")

    st.markdown("""
    <div style="margin-bottom: 3rem;">
        <div style="font-size:2rem; font-weight:600; color:#F8FAFC; letter-spacing:-0.03em; margin-bottom:1rem; line-height:1.2;">
            Real-time face detection<br>and recognition platform.
        </div>
        <div style="font-size:1rem; color:#94A3B8; max-width:600px; line-height:1.6;">
            A professional computer vision pipeline built for low-latency inference. 
            Register identities, stream live webcam feeds, and monitor detection accuracy.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">System Architecture</div>', unsafe_allow_html=True)

    user_count = len(api.get_all_users())

    st.markdown("""
    <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:1rem; margin-bottom:3rem;">
        <div class="premium-card" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
            <i class="ph ph-users" style="font-size:2rem; color:#E2E8F0; margin-bottom:0.75rem;"></i>
            <div style="font-size:0.75rem; color:#64748B; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.25rem;">Total Users</div>
            <div style="font-size:1.75rem; font-weight:700; color:#F8FAFC;">{count}</div>
        </div>
        <div class="premium-card" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
            <i class="ph ph-brain" style="font-size:2rem; color:#E2E8F0; margin-bottom:0.75rem;"></i>
            <div style="font-size:0.75rem; color:#64748B; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.25rem;">Active Model</div>
            <div style="font-size:1.75rem; font-weight:700; color:#3B82F6;">{model}</div>
        </div>
        <div class="premium-card" style="display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
            <i class="ph ph-target" style="font-size:2rem; color:#E2E8F0; margin-bottom:0.75rem;"></i>
            <div style="font-size:0.75rem; color:#64748B; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.25rem;">Threshold</div>
            <div style="font-size:1.75rem; font-weight:700; color:#22C55E;">{thresh}%</div>
        </div>
    </div>
    """.format(count=user_count, model=api.MODEL_NAME, thresh=api.SIMILARITY_THRESHOLD), unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 4])
    with c1:
        if st.button("Register User", key="home_go_register", type="primary", use_container_width=True):
            st.session_state.current_page = "Register"
            st.rerun()
    with c2:
        if st.button("Open Recognition", key="home_go_recognition", use_container_width=True):
            st.session_state.current_page = "Recognition"
            st.rerun()

    st.markdown('<hr style="margin:3rem 0;">', unsafe_allow_html=True)

    st.markdown("""
    <div style="max-width: 600px;">
        <div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1.5rem;">Pipeline Workflow</div>
    """, unsafe_allow_html=True)

    steps = [
        ("ph-camera", "Capture", "Acquire real-time frames from video source"),
        ("ph-bounding-box", "Detect", "Localize faces and extract landmarks"),
        ("ph-vector-three", "Embed", "Generate 512-dimensional feature vector"),
        ("ph-math-operations", "Compare", "Calculate cosine distance against database"),
    ]

    for icon, title, desc in steps:
        st.markdown(f"""
        <div style="display:flex; align-items:flex-start; gap:1rem; margin-bottom:1.25rem;">
            <div style="width:32px; height:32px; border-radius:6px; background-color:#111111; border:1px solid #1A1A1A; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                <i class="ph {icon}" style="color:#E2E8F0; font-size:1.1rem;"></i>
            </div>
            <div>
                <div style="font-size:0.875rem; font-weight:600; color:#F8FAFC; margin-bottom:0.15rem;">{title}</div>
                <div style="font-size:0.75rem; color:#94A3B8;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
