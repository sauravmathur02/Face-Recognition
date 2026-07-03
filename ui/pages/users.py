import streamlit as st

import backend as api

def render():
    st.markdown("""
    <div class="page-title">Registered Users</div>
    <div class="page-subtitle">Browse and manage faces stored in the database</div>
    """, unsafe_allow_html=True)

    users = api.get_all_users()

    search_col, count_col = st.columns([3, 1])
    with search_col:
        query = st.text_input(
            "Search",
            placeholder="🔍  Search by name…",
            key="users_search",
            label_visibility="collapsed",
        )
    with count_col:
        st.markdown(f"""
        <div style="
            padding:0.55rem 1rem;
            background:rgba(59,130,246,0.08);
            border:1px solid rgba(59,130,246,0.25);
            border-radius:10px;
            text-align:center;
            font-size:0.82rem; color:#60A5FA; font-weight:700;
        ">
            {len(users)} user{'s' if len(users)!=1 else ''}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if query:
        users = [u for u in users if query.lower() in u[1].lower()]

    if not users:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:2.5rem;">
            <div style="font-size:2.5rem; margin-bottom:0.8rem;">🙈</div>
            <div style="font-size:1rem; font-weight:700; color:#E2E8F0; margin-bottom:0.4rem;">
                No users found
            </div>
            <div style="font-size:0.85rem; color:#64748B;">
                Try a different search term, or register a new user.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("➕  Register User", key="users_go_register"):
            st.session_state.current_page = "Register"
            st.rerun()
        return

    st.markdown("""
    <div style="
        display:grid; grid-template-columns:60px 1fr 120px;
        gap:0.5rem; padding:0.5rem 1rem;
        font-size:0.7rem; font-weight:700; color:#475569;
        text-transform:uppercase; letter-spacing:0.1em;
        border-bottom:1px solid rgba(255,255,255,0.06);
        margin-bottom:0.4rem;
    ">
        <div>ID</div>
        <div>Name</div>
        <div style="text-align:right;">Action</div>
    </div>
    """, unsafe_allow_html=True)

    for uid, uname in users:
        row_col1, row_col2, row_col3 = st.columns([1, 5, 2])

        with row_col1:
            st.markdown(f"""
            <div style="
                padding:0.6rem 0;
                font-size:0.8rem;
                color:#475569;
                font-weight:700;
                font-family:monospace;
            ">#{uid}</div>
            """, unsafe_allow_html=True)

        with row_col2:
            st.markdown(f"""
            <div style="
                padding:0.6rem 0;
                font-size:0.9rem;
                font-weight:600;
                color:#E2E8F0;
                display:flex; align-items:center; gap:0.5rem;
            ">
                <span style="
                    width:32px; height:32px; border-radius:50%;
                    background:linear-gradient(135deg,#3B82F6,#7C3AED);
                    display:inline-flex; align-items:center;
                    justify-content:center;
                    font-size:0.75rem; font-weight:800; color:white;
                    flex-shrink:0;
                ">{uname[0].upper()}</span>
                {uname}
            </div>
            """, unsafe_allow_html=True)

        with row_col3:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button("🗑  Delete", key=f"del_{uid}", use_container_width=True):
                ok = api.delete_user(uid)
                if ok:
                    st.success(f"Deleted '{uname}'.")
                    st.rerun()
                else:
                    st.error("Failed to delete user.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="height:1px; background:rgba(255,255,255,0.04);
                    margin:0.1rem 0;"></div>
        """, unsafe_allow_html=True)
