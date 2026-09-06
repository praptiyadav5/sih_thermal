"""
UI Aesthetics & Glassmorphism Styling Utility Module
Provides Google Fonts, Glassmorphism CSS, KPI cards, badges, and Plotly theme presets.
"""
import streamlit as st

def inject_custom_css():
    """
    Injects ultra-premium Glassmorphic dark mode CSS styling with targeted,
    high-contrast Streamlit widget rules (sliders, selectboxes, sidebar, metrics).
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Main App Background */
        .stApp {
            background: radial-gradient(circle at 15% 15%, #0F172A 0%, #090D16 60%, #04060A 100%);
            color: #E2E8F0;
        }

        /* Custom Scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #090D16;
        }
        ::-webkit-scrollbar-thumb {
            background: #1E293B;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }

        /* =========================================================
           SIDEBAR HIGH-CONTRAST READABILITY
           ========================================================= */
        section[data-testid="stSidebar"] {
            background-color: #080C14 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] h4 {
            color: #F8FAFC !important;
            font-weight: 700 !important;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div.stMarkdown {
            color: #CBD5E1 !important;
        }

        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
            color: #94A3B8 !important;
        }

        /* Multipage Sidebar Nav Links */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
            background-color: rgba(30, 41, 59, 0.4) !important;
            border-radius: 8px !important;
            margin-bottom: 4px !important;
            padding: 8px 12px !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a * {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
            background-color: rgba(0, 240, 255, 0.15) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(90deg, #2563EB 0%, #0284C7 100%) !important;
        }

        /* =========================================================
           WIDGET LABELS & SLIDER CONTRAST FIXES
           ========================================================= */
        /* Widget Labels */
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] span,
        .stSlider label,
        .stSelectbox label,
        .stRadio label,
        .stTextInput label,
        .stNumberInput label {
            color: #F8FAFC !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            margin-bottom: 4px !important;
        }

        /* Slider Min/Max Tick Markers */
        div[data-testid="stSliderTickBar"] *,
        div[data-testid="stTickBarMin"],
        div[data-testid="stTickBarMax"] {
            color: #94A3B8 !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
        }

        /* Slider Value Bubble */
        div[data-baseweb="slider"] div {
            color: #F8FAFC !important;
        }

        /* Input Controls & Selectboxes */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > input {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] * {
            color: #F8FAFC !important;
        }

        /* Dropdown Popovers */
        div[data-baseweb="popover"] *,
        ul[data-baseweb="menu"] * {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 1.8rem 2.2rem;
            margin-bottom: 1.8rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #FF4B4B 0%, #FF8F00 35%, #00F0FF 80%, #A855F7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.4rem;
        }

        .hero-sub {
            font-size: 1.05rem;
            color: #94A3B8;
        }

        /* Glassmorphism Containers */
        .glass-card {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 1.4rem;
            margin-bottom: 1rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }

        /* KPI Metric Box */
        .metric-box {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 1.2rem 1rem;
            text-align: center;
        }
        .metric-title {
            font-size: 0.8rem;
            font-weight: 600;
            color: #94A3B8;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 1.9rem;
            font-weight: 800;
            color: #F8FAFC;
        }
        .metric-sub {
            font-size: 0.85rem;
            color: #38BDF8;
        }

        /* Status Badges */
        .badge-ansys {
            background: rgba(16, 185, 129, 0.15);
            color: #34D399 !important;
            border: 1px solid rgba(52, 211, 153, 0.4);
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .badge-mock {
            background: rgba(245, 158, 11, 0.15);
            color: #FBBF24 !important;
            border: 1px solid rgba(251, 191, 36, 0.4);
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
        }

        .badge-pill {
            background: rgba(56, 189, 248, 0.15);
            color: #38BDF8 !important;
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 0.25rem 0.65rem;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        /* Streamlit Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(15, 23, 42, 0.6);
            padding: 6px;
            border-radius: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 8px;
            color: #94A3B8;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important;
        }

        /* Buttons */
        .stButton>button[kind="primary"] {
            background: linear-gradient(90deg, #2563EB 0%, #0284C7 100%);
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }

        /* =========================================================
           TEXT VISIBILITY FIXES (inline code, code blocks, radio,
           multiselect tags, metrics, number inputs, dataframes)
           ========================================================= */

        /* Inline <code> tags used inside glass-card HTML (e.g. <code>value</code>) */
        .stMarkdown code, .glass-card code, p code, div code {
            color: #7DD3FC !important;
            background: rgba(56, 189, 248, 0.12) !important;
            padding: 1px 6px !important;
            border-radius: 4px !important;
            font-family: 'Fira Code', monospace !important;
        }

        /* st.code() blocks (e.g. PyMechanical script preview) */
        div[data-testid="stCodeBlock"] {
            background-color: #0B1120 !important;
            border: 1px solid rgba(255, 255, 255, 0.10) !important;
            border-radius: 10px !important;
        }
        div[data-testid="stCodeBlock"] pre,
        div[data-testid="stCodeBlock"] code,
        div[data-testid="stCodeBlock"] span {
            color: #E2E8F0 !important;
            background-color: transparent !important;
        }

        /* Radio button option labels (e.g. location input method selector) */
        .stRadio [role="radiogroup"] label,
        .stRadio [role="radiogroup"] label p,
        .stRadio [role="radiogroup"] label span,
        .stRadio [role="radiogroup"] label div {
            color: #F1F5F9 !important;
        }

        /* Multiselect selected-item tags (e.g. design preset picker) */
        div[data-baseweb="tag"] {
            background-color: rgba(37, 99, 235, 0.85) !important;
        }
        div[data-baseweb="tag"] span,
        div[data-baseweb="tag"] svg {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        /* Number input fields (manual typing controls) */
        div[data-testid="stNumberInput"] input {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
        }
        div[data-testid="stNumberInput"] button {
            background-color: #1E293B !important;
            color: #F8FAFC !important;
        }
        div[data-testid="stNumberInput"] button svg {
            fill: #F8FAFC !important;
        }

        /* Native st.metric widgets */
        [data-testid="stMetricLabel"] * {
            color: #94A3B8 !important;
        }
        [data-testid="stMetricValue"] {
            color: #F8FAFC !important;
        }
        [data-testid="stMetricDelta"] * {
            color: inherit !important;
        }

        /* Dataframes / tables */
        [data-testid="stDataFrame"] {
            background-color: rgba(15, 23, 42, 0.4) !important;
        }

        /* Text areas & captions */
        .stCaption, [data-testid="stCaptionContainer"] * {
            color: #94A3B8 !important;
        }

        /* =========================================================
           HIDE DEFAULT STREAMLIT CHROME (header / footer / menu / badge)
           ========================================================= */
        header[data-testid="stHeader"] {
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
        }
        footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"] {
            visibility: hidden !important;
            height: 0 !important;
        }
        .viewerBadge_container__1QSob, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK {
            display: none !important;
        }

        /* Reclaim the space the header used to occupy */
        .block-container {
            padding-top: 1.5rem !important;
        }
        [data-testid="stSidebarNav"] {
            padding-top: 0.5rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_hero_banner(title, subtitle, badge_text=None):
    badge_html = f'<span class="badge-pill">{badge_text}</span>' if badge_text else ''
    html = f"""
    <div class="hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div class="hero-title">{title}</div>
                <div class="hero-sub">{subtitle}</div>
            </div>
            <div>{badge_html}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def get_plotly_layout_defaults():
    return dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#CBD5E1"),
        margin=dict(l=25, r=25, t=35, b=25)
    )
