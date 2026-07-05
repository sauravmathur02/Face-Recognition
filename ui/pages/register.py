import time
import cv2
import numpy as np
import streamlit as st

import backend as api
from config import MIN_REG_IMAGES
from ui.components import render_header

def render():
    render_header("Register", "Identity Enrollment")

    st.markdown("""
    <div style="max-width: 600px; margin-bottom: 2rem;">
        <div style="font-size:0.875rem; color:#94A3B8; line-height:1.6;">
            Enroll a new subject into the recognition database. Provide a unique identifier and supply at least 
            <strong style="color:#F8FAFC;">3 high-quality images</strong> for accurate feature extraction.
        </div>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input(
        "Subject Name",
        placeholder="e.g. Jane Doe",
        key="reg_name",
    )
    
    if "reg_mode" not in st.session_state:
        st.session_state.reg_mode = "upload"
    if "reg_cam_active" not in st.session_state:
        st.session_state.reg_cam_active = False

    st.markdown('<br>', unsafe_allow_html=True)

    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        is_up = st.session_state.reg_mode == "upload"
        if st.button("File Upload", key="mode_up", use_container_width=True):
            st.session_state.reg_mode = "upload"
            st.session_state.reg_cam_active = False
            api.release_camera()
            st.rerun()
    with c2:
        is_cam = st.session_state.reg_mode == "webcam"
        if st.button("Webcam Capture", key="mode_cam", use_container_width=True):
            st.session_state.reg_mode = "webcam"
            st.rerun()
            
    st.markdown(f"""
    <div style="display:flex; width:100%; border-bottom:1px solid #1A1A1A; margin-bottom:2rem; position:relative;">
        <div style="position:absolute; bottom:-1px; height:2px; background-color:#3B82F6; width:120px; left:{'0' if is_up else '130px'}; transition:all 0.2s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.reg_mode == "upload":
        uploaded = st.file_uploader(
            "Upload image assets",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="reg_uploader",
            label_visibility="collapsed",
        )

        if uploaded:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.5rem; margin:1rem 0;">
                <i class="ph-fill ph-check-circle" style="color:#22C55E;"></i>
                <span style="font-size:0.875rem; font-weight:500; color:#E2E8F0;">{len(uploaded)} assets staged</span>
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(min(len(uploaded), 5))
            for i, f in enumerate(uploaded[:5]):
                with cols[i]:
                    st.markdown('<div style="border-radius:6px; overflow:hidden; border:1px solid #1A1A1A;">', unsafe_allow_html=True)
                    st.image(f, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            if len(uploaded) > 5:
                st.caption(f"and {len(uploaded)-5} more...")

        st.markdown("<br>", unsafe_allow_html=True)
        register_btn = st.button("Enroll Subject", key="reg_upload_submit", type="primary", use_container_width=True)

        if register_btn:
            if not name.strip():
                st.toast("Subject Name is required.", icon="⚠️")
            elif not uploaded or len(uploaded) < MIN_REG_IMAGES:
                st.toast(f"Insufficient assets. Required: {MIN_REG_IMAGES}, Provided: {len(uploaded or [])}.", icon="⚠️")
            else:
                images = []
                for f in uploaded:
                    arr  = np.frombuffer(f.read(), np.uint8)
                    img  = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                    if img is not None:
                        images.append(img)

                with st.spinner("Extracting features..."):
                    ok, msg = api.register_user(name.strip(), images)

                if ok:
                    st.toast(msg, icon="✅")
                else:
                    st.toast(msg, icon="❌")

    else:
        if "webcam_frames" not in st.session_state:
            st.session_state.webcam_frames = []

        count = len(st.session_state.webcam_frames)
        ready = count >= MIN_REG_IMAGES
        
        ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([1, 1, 1.5, 3])
        with ctrl1:
            if st.button("Start Feed", key="reg_start_cam", type="primary", disabled=st.session_state.reg_cam_active, use_container_width=True):
                st.session_state.reg_cam_active = True
                st.toast("Camera Started", icon="📷")
                st.rerun()
        with ctrl2:
            if st.button("Stop Feed", key="reg_stop_cam", disabled=not st.session_state.reg_cam_active, use_container_width=True):
                st.session_state.reg_cam_active = False
                api.release_camera()
                st.toast("Camera Stopped", icon="🛑")
                st.rerun()
        with ctrl3:
            if st.button("Capture Frame", key="reg_capture_btn", type="primary", disabled=not st.session_state.reg_cam_active, use_container_width=True):
                f = api.capture_frame()
                if f is not None:
                    st.session_state.webcam_frames.append(f.copy())

        status_color = "#22C55E" if ready else "#F59E0B"
        status_icon  = "ph-check-circle" if ready else "ph-camera"
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.5rem; margin-top:1rem; margin-bottom:2rem;">
            <div class="badge {'success' if ready else 'warning'}">
                <i class="ph {status_icon}"></i> {count} / {MIN_REG_IMAGES} captures ready
            </div>
        </div>
        """, unsafe_allow_html=True)

        feed_col, gallery_col = st.columns([2, 1.2])

        with feed_col:
            if not st.session_state.reg_cam_active:
                st.markdown("""
                <div class="empty-state" style="padding: 3rem;">
                    <i class="ph ph-video-camera-slash" style="font-size:2rem;"></i>
                    <div class="empty-state-title" style="font-size:0.875rem;">Camera Offline</div>
                </div>
                """, unsafe_allow_html=True)
            feed_placeholder = st.empty()

        with gallery_col:
            if st.session_state.webcam_frames:
                st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; margin-bottom:0.5rem;">Buffer</div>', unsafe_allow_html=True)
                g_cols = st.columns(2)
                for i, f in enumerate(st.session_state.webcam_frames[:4]):
                    with g_cols[i%2]:
                        st.image(cv2.cvtColor(f, cv2.COLOR_BGR2RGB), use_container_width=True)
                        st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
                
                if st.button("Clear Buffer", key="reg_clear_buf", use_container_width=True):
                    st.session_state.webcam_frames = []
                    st.rerun()

                if st.button("Enroll Subject", key="reg_enroll_cam", type="primary", use_container_width=True):
                    if not name.strip():
                        st.toast("Subject Name required.", icon="⚠️")
                    elif not ready:
                        st.toast("Insufficient frames.", icon="⚠️")
                    else:
                        with st.spinner("Extracting..."):
                            ok, msg = api.register_user(name.strip(), st.session_state.webcam_frames)
                        if ok:
                            st.toast(msg, icon="✅")
                            st.session_state.webcam_frames = []
                        else:
                            st.toast(msg, icon="❌")

        if st.session_state.reg_cam_active:
            while st.session_state.reg_cam_active:
                f = api.capture_frame()
                if f is not None:
                    feed_placeholder.image(f, channels="BGR", use_container_width=True)
                else:
                    st.session_state.reg_cam_active = False
                    api.release_camera()
                    st.rerun()
                    break
                time.sleep(0.03)
