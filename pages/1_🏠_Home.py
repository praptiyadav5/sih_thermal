import streamlit as st
from backend.ui_theme import inject_custom_css, render_hero_banner

st.set_page_config(page_title="Home | Thermal Shelter Simulation", page_icon="🏠", layout="wide")
inject_custom_css()

# Safe access to shared session state (in case this page is opened before app.py initializes it)
mat_db = st.session_state.get("mat_db")
shelter_cfg = st.session_state.get("shelter_config", {})
location_name = st.session_state.get("location_name", "Leh, Ladakh, India")
material_count = len(mat_db.get_all_materials()) if mat_db is not None else 14

render_hero_banner(
    title="🏠 Thermal Shelter Simulation & Optimization Platform",
    subtitle="Engineer zero-carbon, passively heated shelters for extreme cold climates — from concept to validated performance in minutes.",
    badge_text="Platform Overview"
)

# ---------------------------------------------------------
# QUICK STATS STRIP
# ---------------------------------------------------------
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Material Library</div>
        <div class="metric-value">{material_count}+</div>
        <div class="metric-sub">Verified thermal materials</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-title">Roof Geometries</div>
        <div class="metric-value">4</div>
        <div class="metric-sub">Rectangular · Gable · Arch · Monoslope</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-title">Climate Coverage</div>
        <div class="metric-value">Global</div>
        <div class="metric-sub">Any city via Open-Meteo search</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-title">Solver</div>
        <div class="metric-value">FEA</div>
        <div class="metric-sub">PyANSYS + transient physics engine</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# THE PROBLEM
# ---------------------------------------------------------
col_problem, col_objective = st.columns([1.4, 1])

with col_problem:
    st.markdown("""
    <div class="glass-card" style="height:100%;">
        <h3 style="color: #00F0FF; margin-top: 0;">🏔️ The High-Altitude Extreme Cold Challenge</h3>
        <p style="font-size: 1.02rem; line-height: 1.65; color: #CBD5E1;">
            High-altitude regions like <b>Ladakh (Leh, Kargil, Dras, Nyoma, Pangong)</b>, the Arctic, the Alps,
            and the Rockies experience severe winter extremes that make conventional construction inefficient
            and expensive to heat:
        </p>
        <ul style="color:#CBD5E1; line-height:1.8;">
            <li><b>Extreme sub-zero cold:</b> ambient winter temperatures drop to <b>-15°C in Leh</b> and as low as <b>-35°C in Dras</b>.</li>
            <li><b>Intense high-altitude solar radiation:</b> the thin atmosphere allows clear-sky irradiance above <b>900–1050 W/m²</b>.</li>
            <li><b>High wind speeds:</b> gale winds of 8–20 m/s accelerate convective heat loss across building envelopes.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_objective:
    st.markdown("""
    <div class="glass-card" style="height:100%; border-left: 4px solid #10B981;">
        <h3 style="color: #10B981; margin-top: 0;">🎯 Platform Objective</h3>
        <p style="font-size: 1.02rem; line-height: 1.65; color: #CBD5E1;">
            Help engineers, architects, and researchers design <b>zero-carbon, passively heated shelters</b>
            that maximize solar gain and minimize envelope heat loss — backed by real thermal physics,
            not guesswork.
        </p>
        <p style="font-size: 0.95rem; color: #94A3B8;">
            Every design decision — materials, thickness, shape, glazing — is quantified in real
            indoor temperature and energy performance before anything is built.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------------
st.subheader("🔄 How It Works")
st.caption("Five guided steps take you from an empty site to a validated, optimized shelter design.")

step_cols = st.columns(5)
steps = [
    ("1", "📐", "Design", "Set dimensions, roof shape, and wall/roof/floor material layers.", "#FF4B4B"),
    ("2", "🌤️", "Climate", "Pull real weather data for any location worldwide, or a cold-region preset.", "#FF8F00"),
    ("3", "⚡", "Simulate", "Run PyANSYS or the built-in transient thermal solver on your design.", "#00F0FF"),
    ("4", "📊", "Analyze", "Inspect indoor temperature trends, heat-loss breakdowns, and 3D heatmaps.", "#A855F7"),
    ("5", "⚖️", "Compare & Optimize", "Benchmark materials and shapes, then auto-search for the best configuration.", "#10B981"),
]

for col, (num, icon, title, desc, color) in zip(step_cols, steps):
    with col:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; height:100%;">
            <div style="font-size:0.75rem; font-weight:700; color:{color}; letter-spacing:1px;">STEP {num}</div>
            <div style="font-size:1.8rem; margin:0.3rem 0;">{icon}</div>
            <div style="font-weight:700; color:#F8FAFC; margin-bottom:0.4rem;">{title}</div>
            <div style="font-size:0.82rem; color:#94A3B8; line-height:1.4;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# CORE CAPABILITIES
# ---------------------------------------------------------
st.subheader("🧰 Core Capabilities")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #FF4B4B; height:100%;">
        <h4 style="color:#FF4B4B; margin-top:0;">📐 Parametric CAD & Envelope</h4>
        <p style="font-size:0.9rem; color:#94A3B8; line-height:1.55;">
            Configure shelter length, width, and height; choose from Gable, Arch, Monoslope, or Rectangular
            roof shapes; and build multi-layer wall, roof, and floor assemblies with live U-value feedback.
        </p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #00F0FF; height:100%;">
        <h4 style="color:#00F0FF; margin-top:0;">⚡ PyANSYS & FEA Simulation</h4>
        <p style="font-size:0.9rem; color:#94A3B8; line-height:1.55;">
            Runs live ANSYS Mechanical PyMechanical APDL scripts when available, and automatically falls
            back to a high-fidelity transient numerical physics engine otherwise — no setup required.
        </p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #10B981; height:100%;">
        <h4 style="color:#10B981; margin-top:0;">🚀 Multi-Objective Optimizer</h4>
        <p style="font-size:0.9rem; color:#94A3B8; line-height:1.55;">
            Automated parameter search across materials, insulation thickness, orientation, and glazing
            ratio to surface the configuration with the best thermal efficiency.
        </p>
    </div>
    """, unsafe_allow_html=True)

f4, f5, f6 = st.columns(3)

with f4:
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #FF8F00; height:100%;">
        <h4 style="color:#FF8F00; margin-top:0;">🌤️ Worldwide Climate Data</h4>
        <p style="font-size:0.9rem; color:#94A3B8; line-height:1.55;">
            Search any city via Open-Meteo geocoding, or start from cold-region presets like Ladakh,
            the Arctic, the Alps, and the Rockies — with manual override controls.
        </p>
    </div>
    """, unsafe_allow_html=True)

with f5:
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #A855F7; height:100%;">
        <h4 style="color:#A855F7; margin-top:0;">📊 Rich Results & 3D Heatmaps</h4>
        <p style="font-size:0.9rem; color:#94A3B8; line-height:1.55;">
            Indoor vs. outdoor temperature trajectories, hourly component heat-loss breakdowns, and a
            3D spatial indoor temperature surface — exportable for reporting.
        </p>
    </div>
    """, unsafe_allow_html=True)

with f6:
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #38BDF8; height:100%;">
        <h4 style="color:#38BDF8; margin-top:0;">⚖️ Preset & Custom Comparison</h4>
        <p style="font-size:0.9rem; color:#94A3B8; line-height:1.55;">
            Benchmark curated design presets side-by-side, or build your own custom comparison across
            any combination of materials and shelter shapes.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# ACTIVE SESSION SNAPSHOT
# ---------------------------------------------------------
with st.expander("📍 Current session snapshot", expanded=False):
    snap1, snap2, snap3 = st.columns(3)
    snap1.metric("Location", location_name)
    snap2.metric("Shelter Shape", shelter_cfg.get("shape", "Rectangular"))
    dims = f"{shelter_cfg.get('length', 6.0)}m × {shelter_cfg.get('width', 4.0)}m × {shelter_cfg.get('height', 2.4)}m"
    snap3.metric("Dimensions", dims)
    st.caption("These carry over automatically as you move through the Design, Climate, and Simulation pages.")

st.divider()

# ---------------------------------------------------------
# CALL TO ACTION
# ---------------------------------------------------------
st.markdown("""
<div class="glass-card" style="text-align:center; padding: 2rem;">
    <h3 style="margin-top:0; color:#F8FAFC;">Ready to design and simulate your thermal shelter?</h3>
    <p style="color:#94A3B8; font-size:1rem; max-width:640px; margin:0 auto 1rem auto;">
        Start with the parametric CAD studio, or jump straight into comparing materials and shapes
        if you already know what you want to test.
    </p>
</div>
""", unsafe_allow_html=True)

cta1, cta2 = st.columns(2)
with cta1:
    if st.button("🚀 Start Shelter Design", type="primary", use_container_width=True):
        st.switch_page("pages/2_📐_Shelter_Design.py")
with cta2:
    if st.button("⚖️ Compare Materials & Shapes", use_container_width=True):
        st.switch_page("pages/6_⚖️_Comparison.py")
