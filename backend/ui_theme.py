"""
Ultra-modern, motion-rich Glassmorphism UI theme for Thermal Shelter Studio.
Features smooth animations, micro-interactions, responsive high-contrast cards, and polished visual feedback.
"""
import streamlit as st
import streamlit.components.v1 as components
from backend.session_state import ensure_session_state


def inject_custom_css():
    ensure_session_state()
    st.markdown(r"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

      :root {
        --bg: #070b14;
        --bg-panel: rgba(15, 23, 42, 0.72);
        --bg-panel-solid: #0f172a;
        --bg-card: rgba(18, 28, 51, 0.65);
        --border: rgba(255, 255, 255, 0.08);
        --border-hover: rgba(59, 130, 246, 0.45);
        --text: #f8fafc;
        --text-muted: #94a3b8;
        --text-faint: #64748b;
        --brand: #3b82f6;
        --brand-glow: rgba(59, 130, 246, 0.35);
        --accent-cyan: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
      }

      /* Global App Reset & Deep Ambient Gradient */
      html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
      }

      .stApp {
        background:
          radial-gradient(circle at 12% 8%, rgba(37, 99, 235, 0.18) 0%, transparent 42%),
          radial-gradient(circle at 88% 18%, rgba(6, 182, 212, 0.12) 0%, transparent 40%),
          radial-gradient(circle at 50% 80%, rgba(30, 58, 138, 0.10) 0%, transparent 50%),
          var(--bg) !important;
        color: var(--text);
        animation: fadeIn 0.4s var(--ease-spring);
      }

      /* =========================================================
         HIDE STREAMLIT DEFAULT HEADER, DECORATION, MENU & FOOTER
         ========================================================= */
      header[data-testid="stHeader"],
      [data-testid="stHeader"],
      [data-testid="stDecoration"],
      [data-testid="stToolbar"],
      #MainMenu,
      footer {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
      }

      /* Keep sidebar collapse/expand trigger accessible */
      [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        z-index: 999999 !important;
        top: 0.6rem !important;
        left: 0.6rem !important;
      }

      .block-container {
        max-width: 1320px;
        padding-top: 1.2rem !important;
        padding-bottom: 3.5rem;
      }

      /* =========================================================
         APOGEE-INSPIRED KEYFRAME ANIMATIONS & EASING SYSTEM
         ========================================================= */
      :root {
        --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
        --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
        --glow-blue: rgba(56, 189, 248, 0.4);
        --glow-cyan: rgba(6, 182, 212, 0.35);
        --glow-emerald: rgba(16, 185, 129, 0.35);
      }

      @keyframes apogeeFadeUp {
        0% {
          opacity: 0;
          transform: translateY(24px);
        }
        100% {
          opacity: 1;
          transform: translateY(0);
        }
      }

      @keyframes apogeeFadeDown {
        0% {
          opacity: 0;
          transform: translateY(-20px);
        }
        100% {
          opacity: 1;
          transform: translateY(0);
        }
      }

      @keyframes apogeeFadeScale {
        0% {
          opacity: 0;
          transform: scale(0.94);
        }
        100% {
          opacity: 1;
          transform: scale(1);
        }
      }

      @keyframes apogeeBarGrow {
        0% {
          transform: scaleY(0);
          opacity: 0.15;
        }
        100% {
          transform: scaleY(1);
          opacity: 1;
        }
      }

      @keyframes apogeeFloat {
        0%, 100% {
          transform: translateY(0px);
        }
        50% {
          transform: translateY(-5px);
        }
      }

      @keyframes apogeeShimmer {
        0% {
          background-position: -200% 0;
        }
        100% {
          background-position: 200% 0;
        }
      }

      @keyframes pulseRing {
        0% {
          box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6);
        }
        70% {
          box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
        }
        100% {
          box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
      }

      /* Animation Utility Classes */
      .anim-fade-up {
        animation: apogeeFadeUp 0.7s var(--ease-spring) forwards;
        will-change: transform, opacity;
      }

      .anim-fade-down {
        animation: apogeeFadeDown 0.6s var(--ease-spring) forwards;
        will-change: transform, opacity;
      }

      .anim-fade-scale {
        animation: apogeeFadeScale 0.75s var(--ease-spring) forwards;
        will-change: transform, opacity;
      }

      .anim-float {
        animation: apogeeFloat 4s ease-in-out infinite;
      }

      .delay-100 { animation-delay: 100ms; }
      .delay-150 { animation-delay: 150ms; }
      .delay-200 { animation-delay: 200ms; }
      .delay-300 { animation-delay: 300ms; }
      .delay-400 { animation-delay: 400ms; }
      .delay-500 { animation-delay: 500ms; }
      .delay-600 { animation-delay: 600ms; }
      .delay-700 { animation-delay: 700ms; }
      .delay-800 { animation-delay: 800ms; }
      .delay-900 { animation-delay: 900ms; }
      .delay-1000 { animation-delay: 1000ms; }

      /* =========================================================
         SIDEBAR STYLING & ANIMATIONS
         ========================================================= */
      section[data-testid="stSidebar"] {
        background: #090e1a !important;
        border-right: 1px solid var(--border) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.35);
      }

      section[data-testid="stSidebar"] > div {
        padding-top: 0.85rem;
      }

      /* Sidebar navigation items */
      section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
        border-radius: 12px !important;
        padding: 10px 14px !important;
        margin: 4px 10px !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid transparent !important;
        transition: all 0.22s var(--ease-spring) !important;
      }

      section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
        background: rgba(30, 41, 59, 0.7) !important;
        border-color: rgba(59, 130, 246, 0.3) !important;
        transform: translateX(4px) !important;
      }

      section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
      }

      section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a * {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 0.93rem !important;
      }

      section[data-testid="stSidebar"] p,
      section[data-testid="stSidebar"] span,
      section[data-testid="stSidebar"] div.stMarkdown {
        color: #cbd5e1;
      }

      section[data-testid="stSidebar"] .stCaption {
        color: #94a3b8;
      }

      /* =========================================================
         TYPOGRAPHY & HEADINGS
         ========================================================= */
      h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em;
      }

      h1 {
        font-size: 2.15rem !important;
        line-height: 1.2 !important;
      }

      h2 {
        font-size: 1.65rem !important;
      }

      h3 {
        font-size: 1.28rem !important;
      }

      p, li {
        color: #cbd5e1;
        line-height: 1.65;
        font-size: 0.96rem;
      }

      /* =========================================================
         HERO BANNER (WITH SUBTLE MOTION & GLOW)
         ========================================================= */
      .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.88) 0%, rgba(17, 24, 39, 0.95) 100%);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid var(--border);
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 1.8rem 2.1rem;
        margin-bottom: 1.4rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 14px 36px -10px rgba(0, 0, 0, 0.55);
        animation: fadeInUp 0.45s var(--ease-spring);
      }

      .hero-banner::after {
        content: "";
        position: absolute;
        top: -60%;
        right: -10%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.18) 0%, transparent 70%);
        pointer-events: none;
      }

      .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #60a5fa;
        font-weight: 700;
        font-size: 0.76rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
      }

      .hero-title {
        color: #f8fafc;
        font-size: 2.15rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.03em;
        margin-bottom: 0.55rem;
        background: linear-gradient(90deg, #ffffff 0%, #e2e8f0 60%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }

      .hero-sub {
        color: #94a3b8;
        font-size: 1.02rem;
        max-width: 900px;
        line-height: 1.6;
        font-weight: 400;
      }

      /* =========================================================
         GLASS CARDS & WORKFLOW UX CARDS (WITH HOVER MOTIONS)
         ========================================================= */
      .glass-card, .ux-card {
        background: var(--bg-card);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid var(--border);
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 1.3rem 1.4rem;
        margin-bottom: 0.95rem;
        box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
        transition: all 0.28s var(--ease-spring);
        position: relative;
        overflow: hidden;
      }

      .glass-card:hover, .ux-card:hover {
        transform: translateY(-4px) scale(1.008);
        border-color: var(--border-hover);
        box-shadow: 0 16px 36px -6px rgba(0, 0, 0, 0.55), 0 0 20px -4px var(--brand-glow);
      }

      .ux-card h4 {
        margin: 0.1rem 0 0.5rem 0;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
      }

      .ux-card p {
        margin: 0;
        color: #94a3b8;
        font-size: 0.92rem;
        line-height: 1.55;
      }

      .step-number {
        width: 32px;
        height: 32px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        color: white;
        font-weight: 800;
        font-size: 0.85rem;
        margin-right: 0.65rem;
        box-shadow: 0 3px 10px rgba(37, 99, 235, 0.35);
        transition: transform 0.2s ease;
      }

      .ux-card:hover .step-number {
        transform: rotate(-6deg) scale(1.1);
      }

      /* Metric boxes */
      [data-testid="stMetric"], .metric-box {
        background: var(--bg-card) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid var(--border) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        padding: 1.05rem 1.15rem !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.25s var(--ease-spring) !important;
      }

      [data-testid="stMetric"]:hover, .metric-box:hover {
        transform: translateY(-3px);
        border-color: rgba(59, 130, 246, 0.4) !important;
        box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.5), 0 0 16px -4px rgba(59, 130, 246, 0.25) !important;
      }

      [data-testid="stMetricLabel"] * {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }

      [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 800 !important;
        font-family: 'JetBrains Mono', monospace !important;
      }

      .metric-title {
        color: #8fa2bb;
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
      }

      .metric-value {
        color: #f8fafc;
        font-size: 1.75rem;
        font-weight: 800;
        margin: 0.2rem 0;
        font-family: 'JetBrains Mono', monospace;
      }

      .metric-sub {
        color: #60a5fa;
        font-size: 0.85rem;
        font-weight: 500;
      }

      /* =========================================================
         BUTTONS & PAGE LINKS WITH HOVER ELEVATION
         ========================================================= */
      .stButton > button {
        min-height: 44px;
        border-radius: 12px;
        font-weight: 650;
        font-size: 0.94rem;
        letter-spacing: -0.01em;
        transition: all 0.24s var(--ease-spring);
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: rgba(30, 41, 59, 0.8);
        color: #f8fafc;
      }

      .stButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(96, 165, 250, 0.5);
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.45);
      }

      .stButton > button:active {
        transform: translateY(0);
      }

      .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 60%, #0284c7 100%);
        border: 1px solid rgba(147, 197, 253, 0.35);
        color: white;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.38);
      }

      .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 60%, #0369a1 100%);
        box-shadow: 0 8px 26px rgba(37, 99, 235, 0.55);
      }

      /* Streamlit page-link pills */
      [data-testid="stPageLink-NavLink"] {
        background: rgba(30, 41, 59, 0.75) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 9px 14px !important;
        transition: all 0.22s var(--ease-spring) !important;
        text-decoration: none !important;
      }

      [data-testid="stPageLink-NavLink"]:hover {
        background: rgba(37, 99, 235, 0.22) !important;
        border-color: rgba(96, 165, 250, 0.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25) !important;
      }

      [data-testid="stPageLink-NavLink"] * {
        color: #f8fafc !important;
        font-weight: 600 !important;
      }

      /* =========================================================
         INPUT WIDGETS (SLIDERS, SELECTBOXES, TABS)
         ========================================================= */
      [data-testid="stWidgetLabel"] p,
      [data-testid="stWidgetLabel"] span {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 0.94rem !important;
      }

      div[data-baseweb="select"] > div,
      div[data-baseweb="input"] > input,
      div[data-testid="stNumberInput"] input,
      textarea {
        background: #0d1424 !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
      }

      div[data-baseweb="select"] > div:focus-within,
      div[data-baseweb="input"] > input:focus,
      div[data-testid="stNumberInput"] input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25) !important;
      }

      div[data-baseweb="popover"] *,
      ul[data-baseweb="menu"] * {
        background: #0d1424 !important;
        color: #f8fafc !important;
      }

      /* Streamlit Tabs */
      .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.85);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid var(--border);
      }

      .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.92rem;
        transition: all 0.2s ease;
        padding: 0 16px;
      }

      .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
      }

      /* Slider thumb and track */
      .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #3b82f6 !important;
        box-shadow: 0 0 12px rgba(59, 130, 246, 0.8) !important;
        border: 2px solid white !important;
      }

      /* =========================================================
         STATUS BADGES & INDICATOR DOTS
         ========================================================= */
      .badge-ansys, .badge-mock, .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        width: max-content;
        padding: 0.32rem 0.75rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
      }

      .badge-ansys {
        color: #86efac !important;
        background: rgba(16, 185, 129, 0.14);
        border: 1px solid rgba(16, 185, 129, 0.35);
      }

      .badge-mock {
        color: #fde047 !important;
        background: rgba(245, 158, 11, 0.14);
        border: 1px solid rgba(245, 158, 11, 0.35);
      }

      .badge-pill {
        color: #93c5fd !important;
        background: rgba(59, 130, 246, 0.14);
        border: 1px solid rgba(59, 130, 246, 0.32);
      }
      /* =========================================================
         APOGEE HERO SECTION & LIVE METRIC CARD STYLES
         ========================================================= */
      .apogee-hero-container {
        display: grid;
        grid-template-columns: 1.15fr 0.85fr;
        gap: 2rem;
        align-items: center;
        background: linear-gradient(145deg, rgba(11, 17, 33, 0.92) 0%, rgba(15, 23, 42, 0.96) 60%, rgba(8, 12, 24, 0.98) 100%);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 2.4rem 2.6rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
      }

      .apogee-hero-bg-video {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        opacity: 0.38;
        pointer-events: none;
        z-index: 0;
        filter: saturate(1.2) brightness(0.85);
      }

      .apogee-hero-video-overlay {
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 40% 40%, rgba(8, 10, 25, 0.42) 0%, rgba(8, 10, 25, 0.88) 100%);
        pointer-events: none;
        z-index: 1;
      }

      .apogee-hero-container::before {
        content: "";
        position: absolute;
        top: -40%;
        left: 20%;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, transparent 65%);
        pointer-events: none;
        z-index: 1;
      }

      .apogee-hero-container::after {
        content: "";
        position: absolute;
        bottom: -30%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.14) 0%, transparent 70%);
        pointer-events: none;
        z-index: 1;
      }

      /* Animated SVG Diagram Keyframes */
      @keyframes sunPulse {
        0%, 100% {
          transform: scale(1);
          filter: drop-shadow(0 0 12px rgba(251, 191, 36, 0.7));
        }
        50% {
          transform: scale(1.08);
          filter: drop-shadow(0 0 24px rgba(245, 158, 11, 0.95));
        }
      }

      @keyframes rayFlow {
        0% {
          stroke-dashoffset: 60;
          opacity: 0.2;
        }
        50% {
          opacity: 1;
        }
        100% {
          stroke-dashoffset: 0;
          opacity: 0.2;
        }
      }

      @keyframes windDrift {
        0% {
          transform: translateX(-30px);
          opacity: 0;
        }
        50% {
          opacity: 0.8;
        }
        100% {
          transform: translateX(50px);
          opacity: 0;
        }
      }

      @keyframes heatConvection {
        0% {
          transform: translateY(0) scale(0.95);
          opacity: 0.3;
        }
        50% {
          opacity: 0.9;
        }
        100% {
          transform: translateY(-24px) scale(1.08);
          opacity: 0;
        }
      }

      .apogee-kicker-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.14);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #93c5fd;
        margin-bottom: 1.1rem;
        backdrop-filter: blur(10px);
      }

      .apogee-live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        display: inline-block;
        animation: pulseRing 2s infinite ease-in-out;
      }

      .apogee-hero-title {
        font-size: 2.45rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.035em;
        color: #ffffff;
        margin-bottom: 1rem;
      }

      .apogee-hero-title span.accent-text {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
      }

      .apogee-hero-sub {
        font-size: 1.05rem;
        line-height: 1.65;
        color: #94a3b8;
        margin-bottom: 1.6rem;
        max-width: 620px;
      }

      .apogee-tag-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 0.5rem;
      }

      .apogee-tag {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 8px;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #cbd5e1;
      }

      /* APOGEE LIVE METRIC & DIURNAL FLUX CARD */
      .apogee-revenue-card {
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-top: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 20px;
        padding: 1.6rem 1.6rem 1.3rem 1.6rem;
        box-shadow: 0 16px 36px -8px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transition: transform 0.3s var(--ease-spring), border-color 0.3s ease, box-shadow 0.3s ease;
      }

      .apogee-revenue-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.35);
        box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.75), 0 0 24px -6px rgba(56, 189, 248, 0.25);
      }

      .apogee-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
      }

      .apogee-card-kicker {
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #94a3b8;
      }

      .apogee-card-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.32);
        color: #6ee7b7;
        font-size: 0.74rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 9999px;
      }

      .apogee-card-val-row {
        display: flex;
        align-items: baseline;
        gap: 12px;
        margin-bottom: 1.25rem;
      }

      .apogee-card-huge-number {
        font-size: 2.25rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.03em;
        color: #ffffff;
      }

      .apogee-card-dimmed {
        color: rgba(255, 255, 255, 0.35);
      }

      .apogee-delta-pill {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
      }

      /* Animated Staggered Bar Chart */
      .apogee-bars-wrapper {
        position: relative;
        height: 110px;
        width: 100%;
        display: flex;
        align-items: flex-end;
        gap: 4px;
        padding: 0 4px;
        margin-bottom: 0.6rem;
      }

      .apogee-chart-gridline {
        position: absolute;
        left: 0;
        right: 0;
        border-bottom: 1px dashed rgba(255, 255, 255, 0.08);
        pointer-events: none;
      }

      .apogee-bar-col {
        flex: 1;
        height: 100%;
        display: flex;
        align-items: flex-end;
        position: relative;
      }

      .apogee-bar-fill {
        width: 100%;
        border-radius: 3px 3px 1px 1px;
        transform-origin: bottom;
        animation: apogeeBarGrow 0.75s var(--ease-spring) forwards;
      }

      .apogee-bar-normal {
        background: linear-gradient(to top, #1e3a8a 0%, #0284c7 60%, #38bdf8 100%);
      }

      .apogee-bar-peak {
        background: linear-gradient(to top, #0369a1 0%, #f59e0b 60%, #fbbf24 100%);
        box-shadow: 0 0 12px rgba(245, 158, 11, 0.5);
      }

      .apogee-time-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.68rem;
        color: #64748b;
        font-family: 'JetBrains Mono', monospace;
        padding: 0 4px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 6px;
        margin-bottom: 1rem;
      }

      .apogee-card-footer-metrics {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        background: rgba(11, 17, 33, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 0.75rem 0.9rem;
      }

      .apogee-footer-metric-label {
        font-size: 0.68rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 2px;
      }

      .apogee-footer-metric-val {
        font-size: 0.92rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: #f1f5f9;
      }

      @media (max-width: 960px) {
        .apogee-hero-container {
          grid-template-columns: 1fr;
          padding: 1.8rem;
        }
      /* Archetype Cards & Interactive Quick-Lab Styling */
      .archetype-card {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.82) 0%, rgba(15, 23, 42, 0.65) 100%);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-top: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 16px;
        padding: 1.3rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.28s var(--ease-spring);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
      }

      .archetype-card:hover {
        transform: translateY(-5px);
        border-color: rgba(56, 189, 248, 0.45);
        box-shadow: 0 16px 36px -6px rgba(0, 0, 0, 0.6), 0 0 24px rgba(56, 189, 248, 0.2);
      }

      .spec-tag {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #cbd5e1;
        font-size: 0.72rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
      }

      .quick-lab-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.92) 0%, rgba(11, 17, 33, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-top: 1px solid rgba(56, 189, 248, 0.5);
        border-radius: 18px;
        padding: 1.6rem 1.8rem;
        box-shadow: 0 20px 48px -12px rgba(0, 0, 0, 0.6), 0 0 24px -6px rgba(56, 189, 248, 0.2);
        margin-bottom: 1.5rem;
      }

      .pulse-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #6ee7b7;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 9999px;
      }
    </style>
    """, unsafe_allow_html=True)


def render_html(html_str: str):
    """Renders raw HTML safely without Markdown parser treating indented lines as code blocks."""
    import re
    cleaned = re.sub(r'<!--.*?-->', '', html_str, flags=re.DOTALL)
    cleaned_lines = [line.strip() for line in cleaned.splitlines()]
    compact_html = "\n".join(line for line in cleaned_lines if line)
    st.markdown(compact_html, unsafe_allow_html=True)


def render_apogee_hero(location="Leh, Ladakh, India", temp_indoor="+18.4", temp_ambient="-16.2", solar_peak="1,048"):
    """
    Renders the ultra-modern Apogee hero section with staggered keyframe entrance
    and an interactive 24-hour diurnal thermal flux bar graph.
    """
    # 24 diurnal bar percentages for a high-altitude winter cycle (00:00 to 23:00)
    diurnal_flux = [
        34, 32, 30, 28, 27, 28,  # 00:00 - 05:00 Night cold
        36, 48, 64, 82, 94, 100, # 06:00 - 11:00 Morning solar climb (Peak at 11:00-12:00)
        96, 90, 82, 74, 62, 50,  # 12:00 - 17:00 Afternoon storage retention
        45, 41, 39, 37, 35, 34   # 18:00 - 23:00 Evening insulation stabilization
    ]

    bars_html = "".join(
        f'<div class="apogee-bar-col" title="Hour {idx:02d}:00 - Thermal Flux: {height}%">'
        f'<div class="{"apogee-bar-fill apogee-bar-peak" if idx == 11 else "apogee-bar-fill apogee-bar-normal"}" '
        f'style="height:{height}%; animation-delay:{500 + idx * 32}ms;"></div>'
        f'</div>'
        for idx, height in enumerate(diurnal_flux)
    )

    hero_html = f"""<div class="apogee-hero-container">
<video class="apogee-hero-bg-video" src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260813_092641_de52eb87-daf2-41db-92cb-7a56eae012a5.mp4" autoplay loop muted playsinline></video>
<div class="apogee-hero-video-overlay"></div>
<div class="anim-fade-up delay-100" style="position:relative; z-index:2;">
<div class="apogee-kicker-pill anim-fade-down delay-150"><span class="apogee-live-dot"></span><span>Next-Gen High-Altitude Thermal Engineering · v2.5</span></div>
<h1 class="apogee-hero-title anim-fade-up delay-200">Design &amp; Simulate Cold-Climate Shelters <span class="accent-text">with Precision Physics.</span></h1>
<p class="apogee-hero-sub anim-fade-up delay-300">Engineer zero-carbon passively heated shelters for extreme sub-zero regions like <b>{location}</b>, the Arctic, and alpine zones. Formulate multi-layer insulation, quantify diurnal solar heat capture, and generate production-ready <b>PyANSYS Mechanical APDL</b> scripts in minutes.</p>
<div class="apogee-tag-strip anim-fade-up delay-400">
<span class="apogee-tag">❄️ Sub-Zero -35°C Rated</span>
<span class="apogee-tag">☀️ {solar_peak} W/m² Clear-Sky Solar</span>
<span class="apogee-tag">📐 4 Roof Topologies</span>
<span class="apogee-tag">⚡ PyANSYS + Transient FEA</span>
</div>
</div>
<div class="anim-fade-scale delay-400" style="position:relative; z-index:2;">
<div class="apogee-revenue-card">
<div class="apogee-card-header"><span class="apogee-card-kicker">24-Hour Diurnal Thermal Flux</span><span class="apogee-card-badge"><span class="apogee-live-dot"></span> Active Boundary</span></div>
<div class="apogee-card-val-row"><div class="apogee-card-huge-number">{temp_indoor}<span class="apogee-card-dimmed">°C</span></div><div class="apogee-delta-pill">▲ +34.6°C vs Ambient ({temp_ambient}°C)</div></div>
<div class="apogee-bars-wrapper"><div class="apogee-chart-gridline" style="bottom:25%;"></div><div class="apogee-chart-gridline" style="bottom:60%;"></div><div class="apogee-chart-gridline" style="bottom:90%;"></div>{bars_html}</div>
<div class="apogee-time-labels"><span>00:00</span><span>06:00</span><span style="color:#fbbf24; font-weight:700;">12:00 (Peak)</span><span>18:00</span><span>23:00</span></div>
<div class="apogee-card-footer-metrics">
<div><div class="apogee-footer-metric-label">Solar Peak</div><div class="apogee-footer-metric-val">{solar_peak} W/m²</div></div>
<div><div class="apogee-footer-metric-label">Envelope U</div><div class="apogee-footer-metric-val">0.24 W/m²K</div></div>
<div><div class="apogee-footer-metric-label">Heating Saved</div><div class="apogee-footer-metric-val" style="color:#34d399;">86.4%</div></div>
</div>
</div>
</div>
</div>"""
    render_html(hero_html)


def render_animated_shelter_graphic():
    """
    Renders an animated high-altitude solar shelter cutaway illustration in an isolated iframe.
    Eliminates HTML sanitizer stripping, prevents raw SVG code printing, and ensures 60fps animations.
    """
    graphic_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: transparent;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #f8fafc;
    overflow: hidden;
  }
  .glass-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(12px);
  }
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.85rem;
    flex-wrap: wrap;
    gap: 8px;
  }
  .kicker {
    font-size: 0.75rem;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    display: block;
    margin-bottom: 2px;
  }
  .title {
    margin: 0;
    font-size: 1.22rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
  }
  .badge-group {
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(6, 182, 212, 0.14);
    border: 1px solid rgba(6, 182, 212, 0.35);
    color: #67e8f9;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 9999px;
  }
  .badge-ansys {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(245, 158, 11, 0.14);
    border: 1px solid rgba(245, 158, 11, 0.35);
    color: #fbbf24;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 9999px;
  }
  .svg-canvas {
    width: 100%;
    height: auto;
    max-height: 380px;
    border-radius: 12px;
    background: radial-gradient(circle at 18% 18%, #131d38 0%, #080d1e 100%);
    border: 1px solid rgba(255,255,255,0.08);
    display: block;
  }
  @keyframes sunPulse {
    0%, 100% { transform: scale(1); opacity: 0.95; }
    50% { transform: scale(1.04); opacity: 1; filter: drop-shadow(0 0 16px rgba(251, 191, 36, 0.7)); }
  }
  .sun-pulse {
    animation: sunPulse 3.5s infinite ease-in-out;
    transform-origin: 760px 85px;
  }
</style>
</head>
<body>
<div class="glass-card">
  <div class="card-header">
    <div>
      <span class="kicker">⚡ Dynamic Physics Visualization</span>
      <h3 class="title">Passive Solar Heat Capture &amp; Convective Storage</h3>
    </div>
    <div class="badge-group">
      <span class="badge-pill">☀️ 1,050 W/m² Solar Input</span>
      <span class="badge-ansys">🌡️ +34°C Thermal Delta</span>
    </div>
  </div>

  <svg class="svg-canvas" viewBox="0 0 920 380">
    <defs>
      <linearGradient id="sunGlow" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#fffbeb" />
        <stop offset="50%" stop-color="#fbbf24" />
        <stop offset="100%" stop-color="#f59e0b" />
      </linearGradient>
      <linearGradient id="warmInterior" x1="0%" y1="100%" x2="0%" y2="0%">
        <stop offset="0%" stop-color="#ea580c" stop-opacity="0.25" />
        <stop offset="50%" stop-color="#f59e0b" stop-opacity="0.18" />
        <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.05" />
      </linearGradient>
      <linearGradient id="wallGradient" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#0284c7" />
        <stop offset="35%" stop-color="#3b82f6" />
        <stop offset="70%" stop-color="#d97706" />
        <stop offset="100%" stop-color="#f59e0b" />
      </linearGradient>
      <linearGradient id="solarRayGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#fef08a" stop-opacity="0.9" />
        <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.1" />
      </linearGradient>
    </defs>

    <rect x="0" y="320" width="920" height="60" fill="#0c1220" />
    <line x1="0" y1="320" x2="920" y2="320" stroke="rgba(255,255,255,0.12)" stroke-width="2" />
    <text x="40" y="350" fill="#64748b" font-family="'JetBrains Mono', monospace" font-size="12">Permafrost Subsoil (-8°C) · XPS Ground Insulation R-3.5</text>

    <g opacity="0.65">
      <path d="M 40 180 Q 90 170 160 185" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,8" fill="none">
        <animate attributeName="stroke-dashoffset" from="40" to="0" dur="2s" repeatCount="indefinite" />
      </path>
      <path d="M 20 220 Q 80 210 170 225" stroke="#38bdf8" stroke-width="2" stroke-dasharray="8,6" fill="none">
        <animate attributeName="stroke-dashoffset" from="40" to="0" dur="1.6s" repeatCount="indefinite" />
      </path>
      <path d="M 50 260 Q 110 250 180 265" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="5,7" fill="none">
        <animate attributeName="stroke-dashoffset" from="40" to="0" dur="2.4s" repeatCount="indefinite" />
      </path>
      <circle cx="90" cy="195" r="2.5" fill="#bae6fd">
        <animate attributeName="cx" from="50" to="190" dur="2s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite" />
      </circle>
      <circle cx="70" cy="235" r="2" fill="#7dd3fc">
        <animate attributeName="cx" from="40" to="180" dur="1.8s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0;1;0" dur="1.8s" repeatCount="indefinite" />
      </circle>
      <text x="30" y="145" fill="#7dd3fc" font-family="'JetBrains Mono', monospace" font-weight="700" font-size="13">❄️ Ambient: -16.5°C (14 m/s Gale Winds)</text>
    </g>

    <g class="sun-pulse">
      <circle cx="760" cy="85" r="46" fill="url(#sunGlow)" />
      <circle cx="760" cy="85" r="62" stroke="rgba(251, 191, 36, 0.3)" stroke-width="2" fill="none" stroke-dasharray="6,4">
        <animateTransform attributeName="transform" type="rotate" from="0 760 85" to="360 760 85" dur="18s" repeatCount="indefinite" />
      </circle>
      <text x="760" y="90" text-anchor="middle" fill="#78350f" font-family="'JetBrains Mono', monospace" font-weight="800" font-size="13">1,050 W/m²</text>
    </g>

    <line x1="720" y1="115" x2="520" y2="230" stroke="url(#solarRayGrad)" stroke-width="4" stroke-dasharray="12,6">
      <animate attributeName="stroke-dashoffset" from="60" to="0" dur="1.5s" repeatCount="indefinite" />
    </line>
    <line x1="740" y1="135" x2="580" y2="250" stroke="url(#solarRayGrad)" stroke-width="3" stroke-dasharray="10,5">
      <animate attributeName="stroke-dashoffset" from="50" to="0" dur="1.8s" repeatCount="indefinite" />
    </line>
    <line x1="700" y1="95" x2="460" y2="210" stroke="url(#solarRayGrad)" stroke-width="3" stroke-dasharray="14,6">
      <animate attributeName="stroke-dashoffset" from="70" to="0" dur="1.4s" repeatCount="indefinite" />
    </line>

    <polygon points="260,320 260,170 380,105 540,105 540,320" fill="url(#warmInterior)" />

    <rect x="236" y="170" width="24" height="150" fill="#1e293b" stroke="rgba(255,255,255,0.15)" rx="2" />
    <rect x="242" y="170" width="12" height="150" fill="#3b82f6" opacity="0.85" />
    <text x="210" y="240" fill="#93c5fd" font-size="11" font-family="'JetBrains Mono', monospace" transform="rotate(-90 210,240)">R-4.2 Multi-Layer Wall</text>

    <polygon points="230,170 380,95 550,95 550,115 380,115 250,185" fill="#1e293b" stroke="rgba(255,255,255,0.15)" />
    <polygon points="240,173 380,101 545,101 545,109 380,109 250,179" fill="#0284c7" opacity="0.9" />

    <line x1="540" y1="140" x2="540" y2="320" stroke="#38bdf8" stroke-width="6" stroke-opacity="0.75" />
    <line x1="545" y1="140" x2="545" y2="320" stroke="#fef08a" stroke-width="3" stroke-opacity="0.8" />
    <text x="560" y="235" fill="#fde047" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="700">South Glazing: SHGC 0.62</text>

    <rect x="270" y="306" width="260" height="14" fill="#d97706" rx="3" opacity="0.9" />
    <text x="400" y="317" text-anchor="middle" fill="#ffffff" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700">High-Thermal Mass Slab (+22°C Storage)</text>

    <g opacity="0.85">
      <path d="M 500 290 Q 520 200 480 150 Q 420 130 360 170 Q 320 220 350 290" stroke="#fb923c" stroke-width="2.5" fill="none" stroke-dasharray="7,5">
        <animate attributeName="stroke-dashoffset" from="50" to="0" dur="2.2s" repeatCount="indefinite" />
      </path>
      <path d="M 460 270 Q 480 220 440 180 Q 400 170 380 230" stroke="#fdba74" stroke-width="1.8" fill="none" stroke-dasharray="5,5">
        <animate attributeName="stroke-dashoffset" from="40" to="0" dur="2.8s" repeatCount="indefinite" />
      </path>
    </g>

    <rect x="335" y="195" width="135" height="46" rx="10" fill="rgba(15,23,42,0.92)" stroke="#10b981" stroke-width="1.5" />
    <circle cx="350" cy="218" r="4" fill="#10b981" />
    <text x="360" y="214" fill="#94a3b8" font-size="10" font-weight="700" font-family="'Plus Jakarta Sans', sans-serif">INDOOR COMFORT</text>
    <text x="360" y="232" fill="#ffffff" font-size="16" font-weight="800" font-family="'JetBrains Mono', monospace">+18.4°C</text>
  </svg>
</div>
</body>
</html>"""
    components.html(graphic_html, height=480, scrolling=False)


def render_hero_banner(title, subtitle, badge_text=None):
    badge_html = f'<span class="badge-pill">{badge_text}</span>' if badge_text else ''
    banner_html = f"""<div class="hero-banner anim-fade-up">
<div class="hero-kicker anim-fade-down delay-100"><span style="font-size: 1rem;">❄️</span> High-Altitude Thermal Engineering Platform</div>
<div style="display:flex; justify-content:space-between; gap:1.2rem; align-items:flex-start; flex-wrap:wrap;">
<div>
<div class="hero-title anim-fade-up delay-200">{title}</div>
<div class="hero-sub anim-fade-up delay-300">{subtitle}</div>
</div>
{badge_html}
</div>
</div>"""
    render_html(banner_html)


def get_plotly_layout_defaults():
    return dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0c1220",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#CBD5E1"),
        margin=dict(l=25, r=25, t=35, b=25),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)")
    )

