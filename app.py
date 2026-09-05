import streamlit as st
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.materials import MaterialDatabase
from backend.weather import ClimateDataManager
from backend.simulation import ThermalSimulationEngine
from backend.ui_theme import inject_custom_css, render_hero_banner
from ansys.mechanical_script import PyMechanicalScriptBuilder

# Streamlit Page Config
st.set_page_config(
    page_title="Thermal Shelter Simulation & Optimization | Global Cold Regions",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Global Glassmorphism CSS Aesthetics
inject_custom_css()

# Shared Session State Initialization
if "mat_db" not in st.session_state:
    st.session_state.mat_db = MaterialDatabase()

if "weather_mgr" not in st.session_state:
    st.session_state.weather_mgr = ClimateDataManager()

if "sim_engine" not in st.session_state:
    st.session_state.sim_engine = ThermalSimulationEngine(st.session_state.mat_db)

# Default Shelter Geometry Configuration
if "shelter_config" not in st.session_state:
    st.session_state.shelter_config = {
        "length": 6.0,
        "width": 4.0,
        "height": 2.4,
        "shape": "Rectangular",
        "window_area": 1.8,
        "door_area": 2.0,
        "orientation_deg": 0.0,
        "window_u_value": 1.6,
        "window_shgc": 0.60,
        "door_u_value": 2.0,
        "infiltration_ach": 0.5,
        "internal_heat_gain_w": 150.0,
        "initial_indoor_temp": 12.0
    }

# Default Wall, Roof, Floor Stacks
if "wall_stack" not in st.session_state:
    st.session_state.wall_stack = st.session_state.mat_db.calculate_layer_stack([
        {"material_id": "mud_brick", "thickness_m": 0.30},
        {"material_id": "xps_insulation", "thickness_m": 0.08}
    ], "wall")

if "roof_stack" not in st.session_state:
    st.session_state.roof_stack = st.session_state.mat_db.calculate_layer_stack([
        {"material_id": "pu_foam", "thickness_m": 0.10},
        {"material_id": "timber_wood", "thickness_m": 0.04}
    ], "roof")

if "floor_stack" not in st.session_state:
    st.session_state.floor_stack = st.session_state.mat_db.calculate_layer_stack([
        {"material_id": "concrete", "thickness_m": 0.15},
        {"material_id": "xps_insulation", "thickness_m": 0.06}
    ], "floor")

# Default Weather Data (Leh, Ladakh)
if "weather_df" not in st.session_state:
    st.session_state.weather_df = st.session_state.weather_mgr.fetch_weather_data("Leh, Ladakh, India", simulation_days=1)
    st.session_state.location_name = "Leh, Ladakh, India"

if "simulation_results" not in st.session_state:
    st.session_state.simulation_results = None

# Sidebar Content
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/000000/house-with-a-lawn.png", width=65)
    st.title("🏔️ Thermal Shelter Sim")
    st.caption("Global Cold Climate Engineering Platform")
    
    st.divider()
    
    # Engine Status Monitor
    builder = PyMechanicalScriptBuilder(st.session_state.shelter_config, st.session_state.weather_df, st.session_state.wall_stack, st.session_state.roof_stack, st.session_state.floor_stack)
    ansys_ok, ansys_msg = builder.check_ansys_availability()
    
    st.markdown("### ⚙️ Thermal Solver Engine")
    if ansys_ok:
        st.markdown('<span class="badge-ansys">🟢 ANSYS PyMechanical Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-mock">🟡 Physics Fallback Active</span>', unsafe_allow_html=True)
        st.caption("PyMechanical not detected on local host. Operating in high-fidelity transient physics numerical mode.")
    
    st.divider()
    st.markdown("### 📍 Active Session Parameters")
    st.write(f"**Location:** {st.session_state.get('location_name', 'Leh, Ladakh, India')}")
    st.write(f"**Wall U-Value:** `{st.session_state.wall_stack['u_value']:.3f} W/m²K`")
    st.write(f"**Roof U-Value:** `{st.session_state.roof_stack['u_value']:.3f} W/m²K`")
    st.write(f"**Dimensions:** `{st.session_state.shelter_config['length']}m × {st.session_state.shelter_config['width']}m × {st.session_state.shelter_config['height']}m`")

# Hero Banner
render_hero_banner(
    title="🏔️ Thermal Shelter Simulation & Optimization Platform",
    subtitle="Parametric ANSYS Thermal Simulation • Open-Meteo Worldwide Weather Search • Material Layer Assemblies • 3D FEA Heatmaps • Multi-Objective Optimizer",
    badge_text="v2.5 Release"
)

# Quick Overview & Navigation Guide
col_h1, col_h2, col_h3 = st.columns(3)

with col_h1:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#00F0FF; margin-top:0;">📐 1. Design & CAD Wireframe</h4>
        <p style="font-size:0.9rem; color:#94A3B8;">Configure building geometry, eave height, roof shapes, door/window openings, and material layer stacks.</p>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#FF8F00; margin-top:0;">🌤️ 2. Global Climate Hub</h4>
        <p style="font-size:0.9rem; color:#94A3B8;">Search ANY city in the world using Open-Meteo geocoding or select cold region presets (Ladakh, Arctic, Alps, Rockies).</p>
    </div>
    """, unsafe_allow_html=True)

with col_h3:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#10B981; margin-top:0;">⚡ 3. FEA Simulation & Results</h4>
        <p style="font-size:0.9rem; color:#94A3B8;">Run PyMechanical APDL or transient physics numerical solver, visualize 3D thermal heatmaps, benchmark, and optimize.</p>
    </div>
    """, unsafe_allow_html=True)

st.info("👈 Navigate through the **7 Pages** in the sidebar to start your shelter simulation!")
