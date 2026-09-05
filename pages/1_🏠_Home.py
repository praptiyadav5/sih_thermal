import streamlit as st
from backend.ui_theme import inject_custom_css, render_hero_banner

st.set_page_config(page_title="Home | Thermal Shelter Simulation", page_icon="🏠", layout="wide")
inject_custom_css()

render_hero_banner(
    title="🏠 Thermal Shelter Simulation & Optimization Engine",
    subtitle="Passive Solar Engineering & FEA Thermal Physics for High-Altitude Cold Regions (Ladakh, Arctic, Alps, Rockies)",
    badge_text="Platform Overview"
)

st.markdown("""
<div class="glass-card">
    <h3 style="color: #00F0FF; margin-top: 0;">🏔️ The High-Altitude Extreme Cold Challenge</h3>
    <p style="font-size: 1.05rem; line-height: 1.6; color: #CBD5E1;">
        High-altitude regions like <b>Ladakh (Leh, Kargil, Dras, Nyoma, Pangong)</b> experience severe winter extremes:
    </p>
    <ul>
        <li><b>Extreme Sub-Zero Cold:</b> Ambient winter temperatures drop to <b>-15°C in Leh</b> and down to <b>-35°C in Dras</b>.</li>
        <li><b>Intense High-Altitude Solar Radiation:</b> Thin atmospheric layer yields clear-sky solar irradiance exceeding <b>900–1050 W/m²</b>.</li>
        <li><b>High Wind Speeds:</b> Severe gale winds (8 to 20 m/s) accelerate convective heat losses across building envelopes.</li>
    </ul>
    <p style="font-size: 1.05rem; color: #38BDF8;">
        <b>Objective:</b> Design zero-carbon, passively heated thermal shelters that maximize solar gain and minimize envelope heat loss.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #FF4B4B;">
        <h4 style="color:#FF4B4B; margin-top:0;">📐 Parametric CAD & Envelope</h4>
        <p style="font-size:0.9rem; color:#94A3B8;">Configure shelter length, width, height, roof shapes (Gable, Arch, Monoslope), wall/roof/floor layer stacks, and window ratios.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #00F0FF;">
        <h4 style="color:#00F0FF; margin-top:0;">⚡ PyAnsys & FEA Simulation</h4>
        <p style="font-size:0.9rem; color:#94A3B8;">Supports live ANSYS Mechanical PyMechanical APDL script execution alongside a high-fidelity transient numerical physics engine.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card" style="border-left: 4px solid #10B981;">
        <h4 style="color:#10B981; margin-top:0;">🚀 Multi-Objective Optimizer</h4>
        <p style="font-size:0.9rem; color:#94A3B8;">Automated parameter search across materials, insulation thickness, orientation, and glazing ratios to achieve maximum thermal efficiency.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("🔄 End-to-End System Workflow")
st.code("""
USER INPUT (Dimensions, Materials, Glazing, Orientation)
          ↓
CLIMATE DATA ENGINE (Open-Meteo Worldwide Search & Geocoding + Manual Override)
          ↓
THERMAL PHYSICS / PYANSYS SOLVER ENGINE (PyMechanical APDL / Numerical Transient FEA)
          ↓
THERMAL RESULTS PROCESSING (Indoor Temp, Heat Flux, Component Heat Loss Breakdown, 3D Heatmaps)
          ↓
COMPARISON & OPTIMIZATION DASHBOARD (Multi-Design Benchmarking & Recommended Optimal Configuration)
""", language="text")

st.divider()

col_act1, col_act2 = st.columns([2, 1])
with col_act1:
    st.markdown("### Ready to start building and simulating your thermal shelter?")

with col_act2:
    if st.button("🚀 Start Shelter Design", type="primary", use_container_width=True):
        st.switch_page("pages/2_📐_Shelter_Design.py")
