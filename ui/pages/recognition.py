import time
import cv2
import textwrap
import streamlit as st
import backend as api
from ui.components import render_header

def render():
    render_header("Recognition", "Real-Time Detection & Inference")

    user_count = api.get_user_count()
    if user_count == 0:
        st.markdown("""
        <div class="empty-state">
            <i class="ph ph-user-minus"></i>
            <div class="empty-state-title">Database Empty</div>
            <div class="empty-state-desc">Register identities to enable recognition.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Register Identity", type="primary"):
            st.session_state.current_page = "Register"
            st.rerun()
        return

    if not api.is_camera_available():
        st.error("Camera source offline.")
        return

    cam_active = st.session_state.get("cam_active", False)

    ctrl1, ctrl2, ctrl3 = st.columns([1, 1, 6])
    with ctrl1:
        start_clicked = st.button("Start Feed", key="rec_start", type="primary", disabled=cam_active, use_container_width=True)
    with ctrl2:
        stop_clicked = st.button("Stop Feed", key="rec_stop", disabled=not cam_active, use_container_width=True)
    with ctrl3:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; align-items:center; height:100%;">
            <div class="badge">
                <i class="ph ph-database" style="color:#64748B;"></i> {user_count} Profiles
            </div>
            <div class="badge" style="margin-left:0.5rem;">
                <i class="ph ph-crosshair" style="color:#64748B;"></i> 89% Threshold
            </div>
        </div>
        """, unsafe_allow_html=True)

    if start_clicked:
        st.session_state.cam_active = True
        st.toast("Recognition Started", icon="📷")
        st.rerun()

    if stop_clicked:
        st.session_state.cam_active = False
        api.release_camera()
        st.toast("Recognition Stopped", icon="🛑")
        st.rerun()

    st.markdown('<hr style="margin:1.5rem 0;">', unsafe_allow_html=True)

    if not st.session_state.get("cam_active", False):
        st.markdown("""
        <div class="empty-state">
            <i class="ph ph-video-camera-slash"></i>
            <div class="empty-state-title">Camera Feed Offline</div>
            <div class="empty-state-desc">Start the feed to begin real-time inference.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    feed_col, result_col = st.columns([2, 1.2])
    
    with feed_col:
        feed_placeholder = st.empty()
    
    with result_col:
        st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">Inference Result</div>', unsafe_allow_html=True)
        result_placeholder = st.empty()

    st.markdown('<hr style="margin:2rem 0;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.75rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem;">Recognition History</div>', unsafe_allow_html=True)
    history_placeholder = st.empty()
    
    if "rec_history" not in st.session_state:
        st.session_state.rec_history = []

    # High-performance inference loop
    while st.session_state.get("cam_active", False):
        t0 = time.time()
        frame = api.capture_frame()
        if frame is None:
            st.session_state.cam_active = False
            api.release_camera()
            st.rerun()
            break
            
        annotated, results = api.recognize_frame(frame)
        frame_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        dt = (time.time() - t0) * 1000

        feed_placeholder.image(frame_rgb, use_container_width=True)

        if not results:
            html = """
            <div class="premium-card" style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding:3rem 1rem; border-style:dashed;">
                <i class="ph ph-scan" style="font-size:2rem; color:#333333; margin-bottom:1rem;"></i>
                <div style="font-size:0.875rem; color:#94A3B8; font-weight:500;">No subjects detected in frame</div>
            </div>
            """
            result_placeholder.markdown(html, unsafe_allow_html=True)
        else:
            cards_html = ""
            for r in results:
                status_class = "success" if r["recognized"] else "danger"
                status_color = "#22C55E" if r["recognized"] else "#EF4444"
                status_icon  = "ph-check-circle" if r["recognized"] else "ph-warning-circle"
                status_text  = "Verified" if r["recognized"] else "Unknown Identity"
                sim_str = f"{r['similarity']:.1f}%"
                
                if r["recognized"]:
                    entry = {
                        "name": r["name"],
                        "time": time.strftime("%H:%M:%S"),
                        "sim": sim_str
                    }
                    if not st.session_state.rec_history:
                        st.session_state.rec_history.insert(0, entry)
                    elif st.session_state.rec_history[0]["name"] == r["name"]:
                        st.session_state.rec_history[0]["time"] = entry["time"]
                        st.session_state.rec_history[0]["sim"] = entry["sim"]
                    else:
                        st.session_state.rec_history.insert(0, entry)
                        if len(st.session_state.rec_history) > 4:
                            st.session_state.rec_history.pop()

                card = textwrap.dedent(f"""
                <div class="premium-card" style="margin-bottom:1rem; border-left: 3px solid {status_color};">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1.5rem;">
                        <div>
                            <div style="font-size:0.7rem; color:#64748B; font-weight:500; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.25rem;">Subject</div>
                            <div style="font-size:1.25rem; font-weight:600; color:#F8FAFC;">{r["name"]}</div>
                        </div>
                        <div class="badge {status_class}">
                            <i class="ph {status_icon}"></i> {status_text}
                        </div>
                    </div>
                    <div style="margin-bottom:1.25rem;">
                        <div style="display:flex; justify-content:space-between; font-size:0.75rem; margin-bottom:0.5rem;">
                            <span style="color:#94A3B8; font-weight:500;">Confidence Score</span>
                            <span style="color:#F8FAFC; font-weight:600;">{sim_str}</span>
                        </div>
                        <div class="progress-bg">
                            <div class="progress-fill {status_class}" style="width: {r['similarity']}%;"></div>
                        </div>
                    </div>
                    <div style="background-color:#050505; border-radius:8px; padding:0.875rem; border:1px solid #1A1A1A;">
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; margin-bottom:0.5rem;">
                            <span style="color:#64748B;">Model</span>
                            <span style="color:#E2E8F0; font-family:monospace;">{api.MODEL_NAME}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem;">
                            <span style="color:#64748B;">Latency</span>
                            <span style="color:#E2E8F0; font-family:monospace;">{dt:.0f} ms</span>
                        </div>
                    </div>
                </div>
                """)
                cards_html += card
            result_placeholder.markdown(cards_html, unsafe_allow_html=True)
            
            if st.session_state.rec_history:
                hist_html = '<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:1rem;">'
                for h in st.session_state.rec_history:
                    hist_html += textwrap.dedent(f"""
                    <div class="premium-card" style="padding:1rem;">
                        <div style="font-size:0.875rem; font-weight:600; color:#F8FAFC; margin-bottom:0.25rem;">{h["name"]}</div>
                        <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#94A3B8;">
                            <span>{h["time"]}</span>
                            <span style="color:#22C55E; font-weight:500;">{h["sim"]}</span>
                        </div>
                    </div>
                    """)
                hist_html += '</div>'
                history_placeholder.markdown(hist_html, unsafe_allow_html=True)
        
        time.sleep(0.03) # Cap framerate slightly to prevent browser lockup
