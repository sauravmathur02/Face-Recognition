CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://unpkg.com/@phosphor-icons/web/src/regular/style.css');
@import url('https://unpkg.com/@phosphor-icons/web/src/fill/style.css');
@import url('https://unpkg.com/@phosphor-icons/web/src/duotone/style.css');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #050505 !important;
    color: #E2E8F0 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid #111111 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

/* Hide Streamlit elements */
#MainMenu, footer, header, [data-testid="stDeployButton"], [data-testid="stToolbar"] { 
    display: none !important; 
}

/* Main Padding */
[data-testid="stMain"] > div {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

/* Primary Button */
[data-testid="stBaseButton-primary"] {
    background-color: #3B82F6 !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stBaseButton-primary"]:hover {
    background-color: #2563EB !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
}
[data-testid="stBaseButton-primary"]:active {
    transform: translateY(0) !important;
}

/* Secondary Button */
[data-testid="stBaseButton-secondary"] {
    background-color: #111111 !important;
    border: 1px solid #2A2A2A !important;
    color: #E2E8F0 !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stBaseButton-secondary"]:hover {
    border-color: #3B82F6 !important;
    background: #171717 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
}
[data-testid="stBaseButton-secondary"]:active {
    transform: translateY(0) !important;
}

/* Inputs */
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background-color: #111111 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 6px !important;
    color: #F8FAFC !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 1px #3B82F6 !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background-color: #111111 !important;
    border: 1px dashed #2A2A2A !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #3B82F6 !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #2A2A2A !important;
    gap: 1.5rem !important;
}
[data-testid="stTabs"] [role="tab"] {
    padding: 0.5rem 0 !important;
    color: #94A3B8 !important;
    font-weight: 500 !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    transition: color 0.2s ease !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: #F8FAFC !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #F8FAFC !important;
    border-bottom-color: #3B82F6 !important;
}

/* Premium Card & Animations */
@keyframes slideUpFade {
    0% { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes pageFadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}

[data-testid="stMain"] > div {
    animation: pageFadeIn 0.3s ease-out;
}

.premium-card {
    background-color: #111111;
    border: 1px solid #1A1A1A;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
    transition: all 0.2s ease;
    animation: slideUpFade 0.25s ease-out forwards;
}
.premium-card:hover {
    border-color: #2A2A2A;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
    transform: translateY(-2px);
}

/* Sidebar Nav */
.nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0.75rem;
    margin: 0.2rem 0;
    border-radius: 6px;
    color: #94A3B8;
    font-weight: 500;
    font-size: 0.875rem;
    transition: all 0.15s ease;
    cursor: pointer;
}
.nav-item i {
    font-size: 1.1rem;
    color: #64748B;
    transition: color 0.15s ease;
}
.nav-item:hover {
    background-color: #111111;
    color: #E2E8F0;
}
.nav-active {
    background-color: #111111;
    color: #F8FAFC;
}
.nav-active i {
    color: #3B82F6;
}

/* Top Header */
.page-header {
    border-bottom: 1px solid #111111;
    padding-bottom: 1.25rem;
    margin-bottom: 2.5rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}
.page-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #F8FAFC;
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}
.page-subtitle {
    font-size: 0.875rem;
    color: #94A3B8;
}

/* Badge */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
    background-color: #111111;
    border: 1px solid #1A1A1A;
    color: #E2E8F0;
    transition: all 0.2s ease;
}
.badge.primary { border-color: rgba(59,130,246,0.3); color: #3B82F6; background: rgba(59,130,246,0.05); }
.badge.success { border-color: rgba(34,197,94,0.3); color: #22C55E; background: rgba(34,197,94,0.05); }

/* Table Row */
.table-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #111111;
    transition: background-color 0.15s ease;
}
.table-row:hover {
    background-color: #0A0A0A;
}
.table-row:last-child { border-bottom: none; }

hr {
    border: none;
    border-top: 1px solid #111111 !important;
    margin: 2rem 0 !important;
}

.text-muted { color: #94A3B8; }
.text-primary { color: #3B82F6; }
.text-success { color: #22C55E; }
.text-warning { color: #F59E0B; }
.text-danger { color: #EF4444; }

/* Custom Progress Bar */
.progress-bg {
    background-color: #111111;
    border: 1px solid #1A1A1A;
    border-radius: 4px;
    height: 6px;
    width: 100%;
    overflow: hidden;
}
.progress-fill {
    background-color: #3B82F6;
    height: 100%;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.progress-fill.success { background-color: #22C55E; }
.progress-fill.warning { background-color: #F59E0B; }
.progress-fill.danger { background-color: #EF4444; }

/* Camera Presentation */
.camera-feed-container {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1A1A1A;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.6);
    background-color: #050505;
}

/* Empty State Base */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
    background-color: transparent;
    border: 1px dashed #2A2A2A;
    border-radius: 12px;
}
.empty-state i {
    font-size: 2.5rem;
    color: #475569;
    margin-bottom: 1rem;
}
.empty-state-title {
    font-size: 1rem;
    font-weight: 600;
    color: #F8FAFC;
    margin-bottom: 0.5rem;
}
.empty-state-desc {
    font-size: 0.875rem;
    color: #94A3B8;
}

</style>
"""
