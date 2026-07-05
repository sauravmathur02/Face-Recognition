import streamlit as st

st.set_page_config(
    page_title="Vision AI | Face Recognition",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import CSS
st.markdown(CSS, unsafe_allow_html=True)

import backend as api
from ui.pages import home, register, recognition, users, settings, about
from ui.components import render_header

_DEFAULTS = {
    "current_page":  "Overview",
    "cam_active":    False,
    "webcam_frames": [],
    "sidebar_open":  True,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def _nav(target: str):
    st.session_state.cam_active = False
    st.session_state.reg_cam_active = False
    api.release_camera()
    st.session_state.current_page = target
    st.rerun()

NAV = [
    ("Overview", "Overview"),
    ("Recognition", "Recognition"),
    ("Register", "Register"),
    ("Users", "Users"),
    ("Settings", "Settings"),
    ("About", "About"),
]

if st.session_state.sidebar_open:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        transform: none !important;
        min-width: 250px !important;
        max-width: 250px !important;
        width: 250px !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        '<div style="padding:1.5rem 1rem 1rem; border-bottom:1px solid #111111; margin-bottom:1rem; display:flex; align-items:center; gap:0.75rem;">'
        '<div style="width:28px; height:28px; border-radius:6px; background-color:#E2E8F0; display:flex; align-items:center; justify-content:center; flex-shrink:0;">'
        '<i class="ph-fill ph-aperture" style="font-size:1.1rem; color:#050505;"></i></div>'
        '<div><div style="font-size:0.875rem; font-weight:600; color:#F8FAFC; letter-spacing:-0.01em;">Vision AI</div>'
        '<div style="font-size:0.65rem; color:#64748B;">Core Recognition</div></div></div>',
        unsafe_allow_html=True,
    )

    if st.button("Close Sidebar", key="sidebar_close", use_container_width=True):
        st.session_state.sidebar_open = False
        st.rerun()

    st.markdown(
        '<div style="font-size:0.65rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; padding:0.5rem 1rem 0.25rem;">Menu</div>',
        unsafe_allow_html=True,
    )

    current = st.session_state.current_page
    for label, page in NAV:
        if current == page:
            # Active state
            st.markdown(
                f'<div style="background-color:#111111; color:#F8FAFC; padding:0.5rem 0.75rem; border-radius:6px; margin:0.25rem 0; font-size:0.875rem; font-weight:500;">{label}</div>',
                unsafe_allow_html=True,
            )
        else:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                _nav(page)

    cam_ok  = api.is_camera_available()
    cam_dot = "#22C55E" if cam_ok else "#EF4444"
    cam_lbl = "Online" if cam_ok else "Offline"
    users_n = api.get_user_count()

    st.markdown('<hr style="margin:1.5rem 0 0.5rem; border-color:#111111;">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.65rem; font-weight:600; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin:0 0 0.5rem; padding:0 0.25rem;">System</p>', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:#94A3B8; padding:0.15rem 0.25rem;"><span>Model</span><span style="color:#22C55E; font-size:0.5rem;">⬤</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:#94A3B8; padding:0.15rem 0.25rem;"><span>Database</span><span style="color:#22C55E; font-size:0.5rem;">⬤</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:#94A3B8; padding:0.15rem 0.25rem;"><span>Camera</span><span style="color:{cam_dot}; font-size:0.5rem;">⬤</span></div>', unsafe_allow_html=True)

if not st.session_state.sidebar_open:
    open_col, _ = st.columns([1, 8])
    with open_col:
        if st.button("Menu", key="sidebar_open_btn", use_container_width=True):
            st.session_state.sidebar_open = True
            st.rerun()
    st.markdown('<hr style="margin:0.5rem 0 1.5rem; border-color:#111111;">', unsafe_allow_html=True)

page = st.session_state.current_page

if   page == "Overview":    home.render()
elif page == "Register":    register.render()
elif page == "Recognition": recognition.render()
elif page == "Users":       users.render()
elif page == "Settings":    settings.render()
elif page == "About":       about.render()
