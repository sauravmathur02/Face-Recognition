CSS = """
<style>
/* ── Google Font ──────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Base Reset ───────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stApp"],
[data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background: #080C14 !important;
    color: #E2E8F0 !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1321 0%, #0A0F1E 100%) !important;
    border-right: 1px solid rgba(59,130,246,0.12) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

/* ── Hide Streamlit chrome ────────────────────────────────────────── */
#MainMenu, footer, header,
[data-testid="stDeployButton"],
[data-testid="stToolbar"] { display: none !important; }

/* ── Main content padding ─────────────────────────────────────────── */
[data-testid="stMain"] > div {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}

/* ── Buttons ──────────────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    border: 1px solid rgba(59,130,246,0.3) !important;
    background: rgba(59,130,246,0.08) !important;
    color: #93C5FD !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1rem !important;
}
[data-testid="stButton"] > button:hover {
    background: rgba(59,130,246,0.18) !important;
    border-color: rgba(59,130,246,0.55) !important;
    color: #BFDBFE !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.2) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Primary action button (class injected via markdown hack) ─────── */
.btn-primary button {
    background: linear-gradient(135deg, #3B82F6, #7C3AED) !important;
    border: none !important;
    color: white !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 24px rgba(59,130,246,0.35) !important;
}
.btn-primary button:hover {
    box-shadow: 0 8px 32px rgba(59,130,246,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ── Danger button ────────────────────────────────────────────────── */
.btn-danger button {
    border-color: rgba(239,68,68,0.35) !important;
    background: rgba(239,68,68,0.08) !important;
    color: #FCA5A5 !important;
}
.btn-danger button:hover {
    background: rgba(239,68,68,0.18) !important;
    border-color: rgba(239,68,68,0.55) !important;
    box-shadow: 0 4px 16px rgba(239,68,68,0.2) !important;
}

/* ── Inputs / Text areas ──────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(59,130,246,0.5) !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
}

/* ── File uploader ────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(59,130,246,0.3) !important;
    border-radius: 14px !important;
}

/* ── Tabs ─────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stTabs"] [role="tab"] {
    color: #64748B !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #3B82F6, #7C3AED) !important;
    color: white !important;
}

/* ── Alerts / Info boxes ──────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: rgba(255,255,255,0.04) !important;
}

/* ── Dividers ─────────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.07) !important;
    margin: 1.2rem 0 !important;
}

/* ── Custom scrollbar ─────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(59,130,246,0.3);
    border-radius: 3px;
}

/* ── Glass Card component ─────────────────────────────────────────── */
.glass-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.6rem;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.glass-card:hover {
    border-color: rgba(59,130,246,0.25);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ── Stat card ────────────────────────────────────────────────────── */
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: all 0.2s;
}
.stat-card:hover {
    border-color: rgba(59,130,246,0.3);
    background: rgba(59,130,246,0.06);
}
.stat-card .value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg,#60A5FA,#A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}
.stat-card .label {
    font-size: 0.78rem;
    color: #64748B;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.25rem;
}

/* ── Badge ────────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.badge-blue   { background:rgba(59,130,246,0.15); color:#60A5FA;  border:1px solid rgba(59,130,246,0.3); }
.badge-green  { background:rgba(34,197,94,0.15);  color:#4ADE80;  border:1px solid rgba(34,197,94,0.3);  }
.badge-red    { background:rgba(239,68,68,0.15);  color:#F87171;  border:1px solid rgba(239,68,68,0.3);  }
.badge-violet { background:rgba(124,58,237,0.15); color:#A78BFA;  border:1px solid rgba(124,58,237,0.3); }

/* ── Page heading ─────────────────────────────────────────────────── */
.page-title {
    font-size: 1.75rem;
    font-weight: 800;
    background: linear-gradient(135deg, #F1F5F9, #94A3B8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    margin-bottom: 0.2rem;
}
.page-subtitle {
    font-size: 0.9rem;
    color: #475569;
    margin-bottom: 1.5rem;
}

/* ── User table row ───────────────────────────────────────────────── */
.user-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    margin-bottom: 0.5rem;
    transition: all 0.2s;
}
.user-row:hover {
    background: rgba(59,130,246,0.06);
    border-color: rgba(59,130,246,0.2);
}

/* ── Settings row ─────────────────────────────────────────────────── */
.setting-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.2rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 0.88rem;
}
.setting-row:last-child { border-bottom: none; }
.setting-label { color: #94A3B8; font-weight: 500; }
.setting-value { color: #E2E8F0; font-weight: 700; font-family: 'Courier New', monospace; }

/* ── Workflow step ────────────────────────────────────────────────── */
.workflow-step {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.9rem 1.2rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    margin-bottom: 0.5rem;
    transition: all 0.2s;
}
.workflow-step:hover {
    background: rgba(59,130,246,0.05);
    border-color: rgba(59,130,246,0.2);
    transform: translateX(4px);
}
.step-num {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg,#3B82F6,#7C3AED);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem; font-weight: 800; color: white;
    flex-shrink: 0;
}

/* ── Recognition result card ──────────────────────────────────────── */
.result-card-ok {
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
}
.result-card-unknown {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
}

/* ── Sidebar nav item active ──────────────────────────────────────── */
.nav-active {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 0.85rem;
    margin: 0 0.5rem 2px;
    background: rgba(59,130,246,0.18);
    border: 1px solid rgba(59,130,246,0.35);
    border-left: 3px solid #3B82F6;
    border-radius: 10px;
    color: #60A5FA;
    font-weight: 600;
    font-size: 0.875rem;
}

/* ── Hero gradient text ───────────────────────────────────────────── */
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FFFFFF 0%, #93C5FD 50%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    letter-spacing: -0.03em;
}
.hero-sub {
    font-size: 1.1rem;
    color: #64748B;
    font-weight: 400;
    margin-top: 0.8rem;
    line-height: 1.6;
}

/* ── Pulsing dot ──────────────────────────────────────────────────── */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}
.dot-pulse { animation: pulse 2s ease-in-out infinite; }

/* ── Fade in ──────────────────────────────────────────────────────── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0);    }
}
.fade-up { animation: fadeUp 0.4s ease both; }
</style>
"""
