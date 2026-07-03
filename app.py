import streamlit as st

st.set_page_config(
    page_title="Face Recognition",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import CSS
st.markdown(CSS, unsafe_allow_html=True)

import backend as api
from ui.pages import home, register, recognition, users, settings, about

_DEFAULTS = {
    "current_page":  "Home",
    "cam_active":    False,
    "webcam_frames": [],
    "sidebar_open":  True,
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def _nav(target: str):
    if st.session_state.current_page == "Recognition":
        st.session_state.cam_active = False
        api.release_camera()
    st.session_state.current_page = target
    st.rerun()

NAV = [
    ("🏠", "Home",        "Home"),
    ("➕", "Register",    "Register"),
    ("🎯", "Recognition", "Recognition"),
    ("👥", "Users",       "Users"),
    ("⚙️", "Settings",    "Settings"),
    ("ℹ️", "About",       "About"),
]

if st.session_state.sidebar_open:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        transform: none !important;
        min-width: 260px !important;
        max-width: 260px !important;
        width: 260px !important;
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
        '<div style="padding:1.2rem 1rem 0.8rem;border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:0.4rem;display:flex;align-items:center;gap:0.7rem;">'
        '<div style="width:40px;height:40px;border-radius:11px;flex-shrink:0;background:linear-gradient(135deg,#3B82F6,#7C3AED);display:flex;align-items:center;justify-content:center;font-size:1.2rem;box-shadow:0 4px 16px rgba(59,130,246,0.35);">🎭</div>'
        '<div><div style="font-size:0.88rem;font-weight:800;color:#F1F5F9;letter-spacing:-0.01em;line-height:1.2;">Face Recognition</div>'
        '<div style="font-size:0.7rem;color:#475569;margin-top:0.05rem;">Interview Assignment</div></div></div>',
        unsafe_allow_html=True,
    )

    if st.button("✕  Close Sidebar", key="sidebar_close", use_container_width=True):
        st.session_state.sidebar_open = False
        st.rerun()

    st.markdown(
        '<div style="font-size:0.62rem;font-weight:700;color:#334155;text-transform:uppercase;letter-spacing:0.13em;padding:0.5rem 1rem 0.3rem;">Navigation</div>',
        unsafe_allow_html=True,
    )

    current = st.session_state.current_page
    for icon, label, page in NAV:
        if current == page:
            st.markdown(
                f'<div class="nav-active"><span>{icon}</span><span>{label}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            if st.button(f"{icon}  {label}", key=f"nav_{page}", use_container_width=True):
                _nav(page)

    cam_ok  = api.is_camera_available()
    cam_dot = "#22C55E" if cam_ok else "#EF4444"
    cam_lbl = "Online" if cam_ok else "Offline"
    users_n = api.get_user_count()

    st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:1rem 0 0.5rem;">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.62rem;font-weight:700;color:#334155;text-transform:uppercase;letter-spacing:0.13em;margin:0 0 0.4rem;padding:0 0.25rem;">System Status</p>', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;color:#475569;padding:0.12rem 0.25rem;"><span>🧠 InsightFace</span><span style="color:#22C55E;font-size:0.6rem;">⬤</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;color:#475569;padding:0.12rem 0.25rem;"><span>🗄️ SQLite</span><span style="color:#22C55E;font-size:0.6rem;">⬤</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;color:#475569;padding:0.12rem 0.25rem;"><span>📹 Camera ({cam_lbl})</span><span style="color:{cam_dot};font-size:0.6rem;">⬤</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;font-size:0.78rem;color:#475569;padding:0.12rem 0.25rem;"><span>👥 Registered</span><span style="color:#60A5FA;font-weight:700;">{users_n}</span></div>', unsafe_allow_html=True)

if not st.session_state.sidebar_open:
    open_col, _ = st.columns([1, 6])
    with open_col:
        if st.button("☰  Menu", key="sidebar_open_btn", use_container_width=True):
            st.session_state.sidebar_open = True
            st.rerun()
    st.markdown('<hr style="margin:0.5rem 0 1rem;">', unsafe_allow_html=True)

page = st.session_state.current_page

if   page == "Home":        home.render()
elif page == "Register":    register.render()
elif page == "Recognition": recognition.render()
elif page == "Users":       users.render()
elif page == "Settings":    settings.render()
elif page == "About":       about.render()
