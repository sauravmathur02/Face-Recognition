import time

import cv2
import streamlit as st

import backend as api

def render():
    st.markdown("""
    <div class="page-title">Face Recognition</div>
    <div class="page-subtitle">Live webcam recognition · cosine similarity · threshold ≥ 89%</div>
    """, unsafe_allow_html=True)

    user_count = api.get_user_count()
    if user_count == 0:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:2.5rem;">
            <div style="font-size:2.5rem;margin-bottom:0.8rem;">👤</div>
            <div style="font-size:1rem;font-weight:700;color:#E2E8F0;margin-bottom:0.4rem;">
                No registered users yet
            </div>
            <div style="font-size:0.85rem;color:#64748B;">
                Register at least one face before running recognition.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("➕  Register a User", key="rec_go_register"):
            st.session_state.current_page = "Register"
            st.rerun()
        return

    if not api.is_camera_available():
        st.error("⚠️  No camera found on device ID 0. Connect a webcam and restart.")
        return

    cam_active = st.session_state.get("cam_active", False)

    ctrl1, ctrl2, ctrl3 = st.columns([1, 1, 3])
    with ctrl1:
        start_clicked = st.button(
            "▶  Start",
            key="rec_start",
            use_container_width=True,
            disabled=cam_active,
        )
    with ctrl2:
        stop_clicked = st.button(
            "⏹  Stop",
            key="rec_stop",
            use_container_width=True,
            disabled=not cam_active,
        )
    with ctrl3:
        st.markdown(
            f'<div style="padding:0.55rem 0.9rem;background:rgba(255,255,255,0.03);'
            f'border:1px solid rgba(255,255,255,0.07);border-radius:10px;'
            f'font-size:0.82rem;color:#94A3B8;display:flex;align-items:center;gap:0.6rem;">'
            f'<span style="color:#60A5FA;font-weight:700;">{user_count}</span>'
            f'&nbsp;face(s) loaded&nbsp;·&nbsp;'
            f'<span style="color:#A78BFA;font-weight:700;">89%</span>&nbsp;threshold</div>',
            unsafe_allow_html=True,
        )

    if start_clicked:
        st.session_state.cam_active = True
        st.rerun()

    if stop_clicked:
        st.session_state.cam_active = False
        api.release_camera()
        st.rerun()

    st.markdown("---")

    if not st.session_state.get("cam_active", False):
        st.markdown("""
        <div style="text-align:center;padding:3rem;
                    background:rgba(255,255,255,0.02);
                    border:1px dashed rgba(255,255,255,0.08);
                    border-radius:18px;color:#334155;font-size:0.9rem;">
            <div style="font-size:3rem;margin-bottom:0.8rem;">📹</div>
            Press <strong style="color:#60A5FA;">▶ Start</strong> to begin live recognition
        </div>
        """, unsafe_allow_html=True)
        return

    feed_col, result_col = st.columns([3, 2])

    frame = api.capture_frame()

    if frame is None:
        st.error("❌ Failed to read from camera. Check your webcam connection.")
        st.session_state.cam_active = False
        api.release_camera()
        return

    annotated, results = api.recognize_frame(frame)
    frame_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    with feed_col:
        st.image(
            frame_rgb,
            channels="RGB",
            use_container_width=True,
            caption="Live recognition feed",
        )

    with result_col:
        st.markdown(
            '<div style="font-size:0.72rem;font-weight:700;color:#475569;'
            'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem;">'
            'Detection Results</div>',
            unsafe_allow_html=True,
        )

        if results:
            for r in results:
                if r["recognized"]:
                    st.markdown(
                        f'<div class="result-card-ok">'
                        f'<div style="font-size:1rem;font-weight:800;color:#4ADE80;">✅ {r["name"]}</div>'
                        f'<div style="font-size:0.82rem;color:#86EFAC;margin-top:0.25rem;">'
                        f'Similarity: <strong>{r["similarity"]:.1f}%</strong></div>'
                        f'<div style="font-size:0.72rem;color:#4ADE80;margin-top:0.1rem;">● Recognized</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="result-card-unknown">'
                        f'<div style="font-size:1rem;font-weight:800;color:#F87171;">❓ Unknown</div>'
                        f'<div style="font-size:0.82rem;color:#FCA5A5;margin-top:0.25rem;">'
                        f'Best match: <strong>{r["similarity"]:.1f}%</strong></div>'
                        f'<div style="font-size:0.72rem;color:#F87171;margin-top:0.1rem;">'
                        f'● Below threshold (89%)</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown(
                '<div style="padding:1.5rem;text-align:center;'
                'background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);'
                'border-radius:14px;color:#334155;font-size:0.85rem;">'
                '<div style="font-size:1.5rem;margin-bottom:0.4rem;">👁️</div>'
                'No faces detected</div>',
                unsafe_allow_html=True,
            )

    time.sleep(0.04)
    st.rerun()
