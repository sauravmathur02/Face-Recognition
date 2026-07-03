import streamlit as st
from config import MODEL_NAME, SIMILARITY_THRESHOLD, DB_PATH, CAMERA_ID

def render():

    st.markdown("""
    <div class="fade-up" style="text-align:center; padding: 2.5rem 1rem 2rem;">
        <div style="
            display:inline-flex; align-items:center; justify-content:center;
            width:72px; height:72px; border-radius:20px;
            background:linear-gradient(135deg,#3B82F6,#7C3AED);
            font-size:2rem; margin-bottom:1.2rem;
            box-shadow: 0 8px 32px rgba(59,130,246,0.4);
        ">🎭</div>
        <div class="hero-title">Face Recognition</div>
        <div class="hero-sub">
            A clean, minimal face recognition pipeline built for an interview assignment.<br>
            Register faces, run live recognition, and manage users — nothing more.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fade-up" style="margin: 0 auto 2.5rem; max-width:700px;">
        <div style="
            display:grid; grid-template-columns:repeat(2,1fr);
            gap:1rem;
        ">
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:1.6rem; margin-bottom:0.5rem;">🧠</div>
                <div style="font-size:0.72rem; color:#64748B; font-weight:700;
                            text-transform:uppercase; letter-spacing:0.1em;">AI Model</div>
                <div style="font-size:1rem; font-weight:700; color:#60A5FA;
                            margin-top:0.25rem;">InsightFace</div>
                <div style="font-size:0.78rem; color:#475569; margin-top:0.1rem;">buffalo_l</div>
            </div>
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:1.6rem; margin-bottom:0.5rem;">🗄️</div>
                <div style="font-size:0.72rem; color:#64748B; font-weight:700;
                            text-transform:uppercase; letter-spacing:0.1em;">Database</div>
                <div style="font-size:1rem; font-weight:700; color:#A78BFA;
                            margin-top:0.25rem;">SQLite</div>
                <div style="font-size:0.78rem; color:#475569; margin-top:0.1rem;">faces.db</div>
            </div>
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:1.6rem; margin-bottom:0.5rem;">🎯</div>
                <div style="font-size:0.72rem; color:#64748B; font-weight:700;
                            text-transform:uppercase; letter-spacing:0.1em;">Recognition Threshold</div>
                <div style="font-size:1.5rem; font-weight:900;
                            background:linear-gradient(135deg,#3B82F6,#7C3AED);
                            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                            margin-top:0.25rem;">89%</div>
                <div style="font-size:0.78rem; color:#475569; margin-top:0.1rem;">Cosine Similarity</div>
            </div>
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:1.6rem; margin-bottom:0.5rem;">📹</div>
                <div style="font-size:0.72rem; color:#64748B; font-weight:700;
                            text-transform:uppercase; letter-spacing:0.1em;">Input</div>
                <div style="font-size:1rem; font-weight:700; color:#4ADE80;
                            margin-top:0.25rem;">Webcam</div>
                <div style="font-size:0.78rem; color:#475569; margin-top:0.1rem;">Camera ID: 0</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom:2.5rem;">
        <div style="font-size:0.85rem; color:#475569; margin-bottom:1.2rem; font-weight:500;">
            Choose where to start
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("➕  Register User", key="home_go_register", use_container_width=True):
            st.session_state.current_page = "Register"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("🎯  Start Recognition", key="home_go_recognition", use_container_width=True):
            st.session_state.current_page = "Recognition"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        if st.button("👥  View Users", key="home_go_users", use_container_width=True):
            st.session_state.current_page = "Users"
            st.rerun()

    st.markdown("""
    <div class="fade-up" style="max-width:640px; margin:0 auto;">
        <div class="glass-card">
            <div style="font-size:0.72rem; font-weight:700; color:#64748B;
                        text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem;">
                How It Works
            </div>
            <div style="display:flex; flex-direction:column; gap:0.5rem;">
    """, unsafe_allow_html=True)

    steps = [
        ("📸", "Capture",  "Webcam frame is captured in real-time"),
        ("🧠", "Detect",   "InsightFace detects and localizes faces"),
        ("📐", "Embed",    "512-d embedding vector is extracted"),
        ("📊", "Compare",  "Cosine similarity against all stored embeddings"),
        ("🗄️", "Match",    "Best match looked up in SQLite (threshold ≥ 89%)"),
        ("✅", "Result",   "Name + confidence displayed on the frame"),
    ]

    flow_html = ""
    for i, (icon, title, desc) in enumerate(steps):
        flow_html += f"""
        <div class="workflow-step">
            <div class="step-num">{i+1}</div>
            <div style="font-size:1rem;">{icon}</div>
            <div>
                <div style="font-size:0.875rem; font-weight:700; color:#E2E8F0;">{title}</div>
                <div style="font-size:0.78rem; color:#64748B; margin-top:0.1rem;">{desc}</div>
            </div>
        </div>
        """
    st.markdown(flow_html + "</div></div></div>", unsafe_allow_html=True)
