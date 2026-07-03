import cv2
import numpy as np
import streamlit as st

import backend as api
from config import MIN_REG_IMAGES

def render():
    st.markdown("""
    <div class="page-title">Register User</div>
    <div class="page-subtitle">Add a new face to the recognition database</div>
    """, unsafe_allow_html=True)

    name = st.text_input(
        "Full Name",
        placeholder="e.g. John Doe",
        key="reg_name",
        label_visibility="visible",
    )

    tab_upload, tab_webcam = st.tabs(["📁  Upload Images", "📸  Webcam Capture"])

    with tab_upload:
        st.markdown(f"""
        <div style="font-size:0.82rem; color:#64748B; margin-bottom:0.8rem;">
            Upload at least <strong style="color:#60A5FA;">{MIN_REG_IMAGES} photos</strong>
            with a clear, front-facing face. More photos = better accuracy.
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Choose image files",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="reg_uploader",
            label_visibility="collapsed",
        )

        if uploaded:
            st.markdown(f"""
            <div style="font-size:0.82rem; color:#4ADE80; margin:0.5rem 0;">
                ✓ {len(uploaded)} file(s) selected
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(min(len(uploaded), 5))
            for i, f in enumerate(uploaded[:5]):
                with cols[i]:
                    st.image(f, use_container_width=True)
            if len(uploaded) > 5:
                st.caption(f"+ {len(uploaded)-5} more file(s)")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        register_btn = st.button(
            "✅  Register Face", key="reg_upload_submit", use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if register_btn:
            if not name.strip():
                st.error("Please enter a name first.")
            elif not uploaded or len(uploaded) < MIN_REG_IMAGES:
                st.error(
                    f"Please upload at least {MIN_REG_IMAGES} images "
                    f"(you uploaded {len(uploaded or [])})."
                )
            else:
                images = []
                for f in uploaded:
                    arr  = np.frombuffer(f.read(), np.uint8)
                    img  = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                    if img is not None:
                        images.append(img)

                with st.spinner("Processing and registering…"):
                    ok, msg = api.register_user(name.strip(), images)

                if ok:
                    st.success(f"🎉 {msg}")
                    st.balloons()
                else:
                    st.error(f"❌ {msg}")

    with tab_webcam:
        st.markdown(f"""
        <div style="font-size:0.82rem; color:#64748B; margin-bottom:0.8rem;">
            Capture at least <strong style="color:#60A5FA;">{MIN_REG_IMAGES} photos</strong>
            from your webcam. Vary your pose slightly between captures.
        </div>
        """, unsafe_allow_html=True)

        if "webcam_frames" not in st.session_state:
            st.session_state.webcam_frames = []

        count = len(st.session_state.webcam_frames)
        ready = count >= MIN_REG_IMAGES
        status_color  = "#4ADE80" if ready else "#F59E0B"
        status_text   = f"{'✓ Ready to register' if ready else f'{count}/{MIN_REG_IMAGES} captures'}"

        st.markdown(f"""
        <div style="
            display:flex; align-items:center; gap:0.75rem;
            padding:0.6rem 1rem;
            background: rgba(255,255,255,0.03);
            border:1px solid rgba(255,255,255,0.07);
            border-radius:10px;
            margin-bottom:0.8rem;
        ">
            <span style="font-size:1.2rem;">📷</span>
            <span style="color:{status_color}; font-weight:700; font-size:0.9rem;">
                {status_text}
            </span>
        </div>
        """, unsafe_allow_html=True)

        cam_col1, cam_col2, cam_col3 = st.columns([1, 1, 1])

        with cam_col1:
            if st.button("📸  Capture Frame", key="reg_capture", use_container_width=True):
                frame = api.capture_frame()
                if frame is None:
                    st.error("Camera not available.")
                else:
                    st.session_state.webcam_frames.append(frame.copy())
                    st.rerun()

        with cam_col2:
            if st.button("🗑️  Clear All", key="reg_clear_webcam", use_container_width=True):
                st.session_state.webcam_frames = []
                st.rerun()

        with cam_col3:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            webcam_register_btn = st.button(
                "✅  Register", key="reg_webcam_submit", use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.webcam_frames:
            frames = st.session_state.webcam_frames
            cols   = st.columns(min(len(frames), 5))
            for i, f in enumerate(frames[:5]):
                with cols[i]:
                    st.image(
                        cv2.cvtColor(f, cv2.COLOR_BGR2RGB),
                        use_container_width=True,
                        caption=f"#{i+1}",
                    )
            if len(frames) > 5:
                st.caption(f"+ {len(frames)-5} more captured")

        if webcam_register_btn:
            if not name.strip():
                st.error("Please enter a name first.")
            elif not ready:
                st.error(
                    f"Please capture at least {MIN_REG_IMAGES} frames "
                    f"(captured {count})."
                )
            else:
                with st.spinner("Processing and registering…"):
                    ok, msg = api.register_user(
                        name.strip(), st.session_state.webcam_frames
                    )
                if ok:
                    st.success(f"🎉 {msg}")
                    st.session_state.webcam_frames = []
                    st.balloons()
                else:
                    st.error(f"❌ {msg}")
