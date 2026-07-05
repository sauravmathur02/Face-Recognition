import streamlit as st
from datetime import datetime

def render_header(title: str, subtitle: str):
    now = datetime.now().strftime("%b %d, %Y • %I:%M %p")
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">{title}</div>
            <div class="page-subtitle">{subtitle}</div>
        </div>
        <div style="font-size:0.75rem; color:#64748B; font-weight:500; display:flex; align-items:center; gap:0.4rem;">
            <i class="ph ph-clock"></i> {now}
        </div>
    </div>
    """, unsafe_allow_html=True)
