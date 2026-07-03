import streamlit as st
from config import MODEL_NAME, SIMILARITY_THRESHOLD, DB_PATH

def render():
    st.markdown("""
    <div class="page-title">About</div>
    <div class="page-subtitle">How this Face Recognition works</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card fade-up" style="margin-bottom:1.5rem;">
        <div style="display:flex; align-items:flex-start; gap:1.2rem;">
            <div style="
                width:52px; height:52px; border-radius:14px;
                background:linear-gradient(135deg,#3B82F6,#7C3AED);
                display:flex; align-items:center; justify-content:center;
                font-size:1.5rem; flex-shrink:0;
            ">🎭</div>
            <div>
                <div style="font-size:1.1rem; font-weight:800; color:#F1F5F9;
                            margin-bottom:0.4rem;">Face Recognition</div>
                <div style="font-size:0.875rem; color:#64748B; line-height:1.7;">
                    A minimal, interview-ready face recognition pipeline built with
                    <strong style="color:#60A5FA;">InsightFace (buffalo_l)</strong>,
                    <strong style="color:#A78BFA;">SQLite</strong>, and
                    <strong style="color:#4ADE80;">Streamlit</strong>.
                    The system registers faces from uploaded images or webcam captures,
                    stores average embeddings, and performs real-time recognition using
                    cosine similarity with a fixed threshold of
                    <strong style="color:#FBBF24;">89%</strong>.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.72rem; font-weight:700; color:#64748B;
                text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.8rem;">
        Recognition Workflow
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("📹", "Camera Input",
         "OpenCV captures a BGR frame from Camera ID 0 at ~25 fps."),
        ("🧠", "InsightFace Detection",
         "buffalo_l detects face bounding boxes and landmarks on a 320×320 input."),
        ("📐", "Embedding Extraction",
         "A 512-dimensional float32 vector is extracted for each detected face."),
        ("📏", "L2 Normalization",
         "Each embedding is divided by its L2 norm so dot product = cosine similarity."),
        ("📊", "Cosine Similarity Search",
         "Vectorized dot product against all stored embeddings (numpy, O(n))."),
        ("🗄️", "SQLite Lookup",
         "The best-matching name is retrieved from faces.db if similarity ≥ 89%."),
        ("✅", "Recognition Result",
         "Name + similarity % drawn on the frame; 'Unknown' shown if below threshold."),
    ]

    for i, (icon, title, desc) in enumerate(steps):
        connector = (
            '<div style="width:2px; height:16px; background:linear-gradient('
            '135deg,#3B82F6,#7C3AED); margin-left:15px; margin-bottom:0;"></div>'
            if i < len(steps) - 1 else ""
        )
        st.markdown(f"""
        <div class="workflow-step fade-up">
            <div class="step-num">{i+1}</div>
            <div style="font-size:1.1rem;">{icon}</div>
            <div>
                <div style="font-size:0.9rem; font-weight:700; color:#E2E8F0;">{title}</div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:0.15rem; line-height:1.5;">{desc}</div>
            </div>
        </div>
        {connector}
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:1.5rem; margin-bottom:0.6rem;">
        <div style="font-size:0.72rem; font-weight:700; color:#64748B;
                    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem;">
            Tech Stack
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
            <span class="badge badge-blue">InsightFace</span>
            <span class="badge badge-violet">buffalo_l</span>
            <span class="badge badge-green">SQLite</span>
            <span class="badge badge-blue">OpenCV</span>
            <span class="badge badge-violet">NumPy</span>
            <span class="badge badge-blue">Streamlit</span>
            <span class="badge badge-green">Python 3.10+</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1.5rem;">
        <div class="glass-card">
            <div style="font-size:0.72rem; font-weight:700; color:#64748B;
                        text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.8rem;">
                Registration
            </div>
            <div style="font-size:0.82rem; color:#94A3B8; line-height:1.8;">
                ① Enter name<br>
                ② Upload ≥ 3 images <em>or</em> capture from webcam<br>
                ③ Validate each image (1 face, confidence ≥ 0.6, area ≥ 4000 px²)<br>
                ④ Extract 512-d embeddings<br>
                ⑤ Average → L2-normalize<br>
                ⑥ INSERT into <code>faces (name, embedding)</code>
            </div>
        </div>
        <div class="glass-card">
            <div style="font-size:0.72rem; font-weight:700; color:#64748B;
                        text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.8rem;">
                Recognition
            </div>
            <div style="font-size:0.82rem; color:#94A3B8; line-height:1.8;">
                ① Open webcam (Camera ID 0)<br>
                ② Detect faces in each frame<br>
                ③ Extract + normalize embedding<br>
                ④ Dot-product against all rows in DB<br>
                ⑤ If max score ≥ 89% → <strong style="color:#4ADE80;">Recognized</strong><br>
                ⑥ Otherwise → <strong style="color:#F87171;">Unknown</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
