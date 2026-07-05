import time
import streamlit as st
import backend as api
from ui.components import render_header

def render():
    render_header("Identities", "Manage Registered Subjects")

    users = api.get_all_users()

    search_col, count_col = st.columns([3, 1])
    with search_col:
        query = st.text_input(
            "Search",
            placeholder="Search subjects...",
            key="users_search",
            label_visibility="collapsed",
        )
    with count_col:
        st.markdown(f"""
        <div style="height:100%; display:flex; align-items:center; justify-content:flex-end;">
            <div class="badge primary" style="font-size:0.875rem; padding:0.4rem 0.75rem;">
                <i class="ph ph-users"></i> {len(users)} Subjects
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if query:
        users = [u for u in users if query.lower() in u[1].lower()]

    if not users:
        st.markdown("""
        <div class="premium-card" style="text-align:center; padding:4rem;">
            <i class="ph ph-magnifying-glass" style="font-size:2.5rem; color:#475569; margin-bottom:1rem; display:block;"></i>
            <div style="font-size:1rem; font-weight:600; color:#F8FAFC; margin-bottom:0.5rem;">No subjects found</div>
            <div style="font-size:0.875rem; color:#94A3B8;">Adjust your search or enroll a new identity.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("""
    <div style="display:grid; grid-template-columns:80px 1fr 120px; gap:1rem; padding:0.5rem 1rem; font-size:0.75rem; font-weight:600; color:#64748B; text-transform:uppercase; letter-spacing:0.05em; border-bottom:1px solid #111111; margin-bottom:0.5rem;">
        <div>ID</div>
        <div>Subject Name</div>
        <div style="text-align:right;">Actions</div>
    </div>
    """, unsafe_allow_html=True)

    for idx, (uid, uname) in enumerate(users, start=1):
        row_col1, row_col2, row_col3 = st.columns([0.8, 5, 1.2])

        with row_col1:
            st.markdown(f'<div style="padding:0.75rem 0; font-size:0.875rem; color:#64748B; font-family:monospace;">{idx:04d}</div>', unsafe_allow_html=True)

        with row_col2:
            st.markdown(f"""
            <div style="padding:0.6rem 0; font-size:0.9rem; font-weight:500; color:#F8FAFC; display:flex; align-items:center; gap:0.75rem;">
                <div style="width:28px; height:28px; border-radius:4px; background-color:#111111; border:1px solid #1A1A1A; display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:600; color:#94A3B8;">
                    {uname[0].upper()}
                </div>
                {uname}
            </div>
            """, unsafe_allow_html=True)

        with row_col3:
            if st.button("Revoke", key=f"del_{uid}", use_container_width=True):
                ok = api.delete_user(uid)
                if ok:
                    st.toast("Identity Revoked", icon="🗑️")
                    time.sleep(0.5) # Give toast a moment to register before rerun
                    st.rerun()
                else:
                    st.toast("Failed to revoke identity.", icon="❌")
        
        st.markdown('<div style="height:1px; background-color:#111111; margin:0.25rem 0;"></div>', unsafe_allow_html=True)
