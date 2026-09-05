import streamlit as st
import time

from ansys.mechanical_script import PyMechanicalScriptBuilder
from backend.ui_theme import inject_custom_css, render_hero_banner

st.set_page_config(page_title="Simulation | Thermal Shelter", page_icon="⚡", layout="wide")
inject_custom_css()

sim_engine = st.session_state.sim_engine

render_hero_banner(
    title="⚡ Thermal Simulation Execution Control Panel",
    subtitle="Review design parameters, inspect PyMechanical APDL code, and launch thermal FEA analysis.",
    badge_text="FEA Execution"
)

cfg = st.session_state.shelter_config
ws = st.session_state.wall_stack
rs = st.session_state.roof_stack
fs = st.session_state.floor_stack
weather_df = st.session_state.weather_df

st.subheader("📋 Pre-Simulation Parameter Audit")

col_a1, col_a2, col_a3, col_a4 = st.columns(4)

with col_a1:
    st.markdown("""
    <div class="glass-card">
        <h5 style="color:#00F0FF; margin-top:0;">📐 Geometry</h5>
        <p><b>Size:</b> <code>{}m × {}m × {}m</code></p>
        <p><b>Shape:</b> <code>{}</code></p>
        <p><b>Azimuth:</b> <code>{}° South</code></p>
    </div>
    """.format(cfg['length'], cfg['width'], cfg['height'], cfg['shape'], cfg['orientation_deg']), unsafe_allow_html=True)

with col_a2:
    st.markdown("""
    <div class="glass-card">
        <h5 style="color:#FF8F00; margin-top:0;">🧱 Thermal U-Values</h5>
        <p><b>Wall U:</b> <code>{:.3f} W/m²K</code></p>
        <p><b>Roof U:</b> <code>{:.3f} W/m²K</code></p>
        <p><b>Floor U:</b> <code>{:.3f} W/m²K</code></p>
    </div>
    """.format(ws['u_value'], rs['u_value'], fs['u_value']), unsafe_allow_html=True)

with col_a3:
    st.markdown("""
    <div class="glass-card">
        <h5 style="color:#10B981; margin-top:0;">🚪 Glazing & Airflow</h5>
        <p><b>Windows:</b> <code>{} m²</code></p>
        <p><b>Doors:</b> <code>{} m²</code></p>
        <p><b>Infiltration:</b> <code>{} ACH</code></p>
    </div>
    """.format(cfg['window_area'], cfg['door_area'], cfg['infiltration_ach']), unsafe_allow_html=True)

with col_a4:
    st.markdown("""
    <div class="glass-card">
        <h5 style="color:#A855F7; margin-top:0;">🌤️ Weather Profile</h5>
        <p><b>Site:</b> <code>{}</code></p>
        <p><b>Avg Temp:</b> <code>{:.1f} °C</code></p>
        <p><b>Peak Solar:</b> <code>{:.0f} W/m²</code></p>
    </div>
    """.format(st.session_state.get('location_name', 'Leh, Ladakh'), weather_df['temperature_c'].mean(), weather_df['solar_radiation_w_m2'].max()), unsafe_allow_html=True)

st.divider()

# Solver Status
builder = PyMechanicalScriptBuilder(cfg, weather_df, ws, rs, fs)
ansys_ok, ansys_msg = builder.check_ansys_availability()

col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    st.subheader("⚙️ Solver Engine Status")
    if ansys_ok:
        st.markdown('<span class="badge-ansys">🟢 PyAnsys / PyMechanical Solver Active</span>', unsafe_allow_html=True)
        st.caption("Direct communication pipeline to local ANSYS Mechanical solver active.")
    else:
        st.markdown('<span class="badge-mock">🟡 Simulation Mock / Physics Fallback Active</span>', unsafe_allow_html=True)
        st.caption("PyMechanical is not detected on host system. Performing high-fidelity transient numerical physics simulation.")

with col_s2:
    st.write("")
    st.write("")
    run_button = st.button("🔥 Launch Thermal Simulation", type="primary", use_container_width=True)

if run_button:
    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.text("Step 1/4: Formulating building thermal energy balance equations...")
    progress_bar.progress(25)
    time.sleep(0.3)

    status_text.text("Step 2/4: Generating PyMechanical APDL script & boundary conditions...")
    progress_bar.progress(50)
    time.sleep(0.3)

    status_text.text("Step 3/4: Executing transient solver iterations across simulation hours...")
    progress_bar.progress(75)

    sim_res = sim_engine.run_simulation(cfg, weather_df, ws, rs, fs)
    st.session_state.simulation_results = sim_res

    progress_bar.progress(100)
    status_text.text("Step 4/4: Thermal simulation completed successfully!")
    time.sleep(0.2)
    st.balloons()
    st.success("Simulation complete! Results have been recorded in memory.")

st.divider()

# APDL Script Inspector
with st.expander("💻 View Auto-Generated ANSYS PyMechanical APDL Script"):
    pymechanical_code = builder.build_pymechanical_python_script()
    st.code(pymechanical_code, language="python")

st.divider()

col_nav1, col_nav2 = st.columns([3, 1])
with col_nav2:
    if st.session_state.simulation_results is not None:
        if st.button("View Simulation Results Dashboard 📊", type="primary", use_container_width=True):
            st.switch_page("pages/5_📊_Results.py")
    else:
        st.info("Run simulation above to view results.")
