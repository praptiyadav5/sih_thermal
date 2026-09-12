"""
Session State Manager for Thermal Shelter Studio.
Ensures all essential data structures, engines, configurations, and climate caches
are initialized regardless of which page the user accesses first.
"""
import streamlit as st
from backend.materials import MaterialDatabase
from backend.weather import ClimateDataManager
from backend.simulation import ThermalSimulationEngine


def ensure_session_state():
    """Initializes all required session state variables if they do not exist."""
    if "mat_db" not in st.session_state or st.session_state.mat_db is None:
        st.session_state.mat_db = MaterialDatabase()

    if "weather_mgr" not in st.session_state or st.session_state.weather_mgr is None:
        st.session_state.weather_mgr = ClimateDataManager()

    if "sim_engine" not in st.session_state or st.session_state.sim_engine is None:
        st.session_state.sim_engine = ThermalSimulationEngine(st.session_state.mat_db)

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
            "initial_indoor_temp": 12.0,
        }

    if "wall_stack" not in st.session_state:
        st.session_state.wall_stack = st.session_state.mat_db.calculate_layer_stack([
            {"material_id": "mud_brick", "thickness_m": 0.30},
            {"material_id": "xps_insulation", "thickness_m": 0.08},
        ], "wall")

    if "roof_stack" not in st.session_state:
        st.session_state.roof_stack = st.session_state.mat_db.calculate_layer_stack([
            {"material_id": "pu_foam", "thickness_m": 0.10},
            {"material_id": "timber_wood", "thickness_m": 0.04},
        ], "roof")

    if "floor_stack" not in st.session_state:
        st.session_state.floor_stack = st.session_state.mat_db.calculate_layer_stack([
            {"material_id": "concrete", "thickness_m": 0.15},
            {"material_id": "xps_insulation", "thickness_m": 0.06},
        ], "floor")

    if "location_name" not in st.session_state:
        st.session_state.location_name = "Leh, Ladakh, India"

    if "weather_df" not in st.session_state or st.session_state.weather_df is None:
        st.session_state.weather_df = st.session_state.weather_mgr.fetch_weather_data(
            st.session_state.location_name, simulation_days=1
        )

    if "simulation_results" not in st.session_state:
        st.session_state.simulation_results = None
