import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from backend.optimizer import ThermalOptimizer
from backend.ui_theme import inject_custom_css, render_hero_banner

st.set_page_config(page_title="Optimization | Thermal Shelter", page_icon="🚀", layout="wide")
inject_custom_css()

mat_db = st.session_state.mat_db
weather_df = st.session_state.weather_df
base_cfg = st.session_state.shelter_config

render_hero_banner(
    title="🚀 Automated Multi-Objective Thermal Optimization",
    subtitle="Searches optimal combinations of wall materials, insulation thicknesses, orientation azimuths, and glazing areas to maximize passive solar gain and minimize heat loss.",
    badge_text="Multi-Objective Optimizer"
)

st.info("The optimizer runs a multi-objective physics search over the parameter space to find shelter designs that maintain indoor comfort ($\ge 18^\circ C$) with minimum heat loss.")

col_opt1, col_opt2 = st.columns([1, 1])

with col_opt1:
    st.subheader("🎯 Optimization Objectives & Constraints")
    target_temp = st.slider("Target Indoor Comfort Temperature (°C)", 15.0, 24.0, 18.0, 0.5)
    max_insulation_cm = st.slider("Max Allowed Insulation Thickness (cm)", 5, 25, 15, 1)

with col_opt2:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#00F0FF; margin-top:0;">Search Space Parameters</h4>
        <ul>
            <li><b>Wall Materials:</b> Mud Brick, Compressed Earth Block (CEB), Granite Stone</li>
            <li><b>Insulation Types:</b> XPS Board, PU Foam Board, Mineral Wool</li>
            <li><b>Insulation Thickness:</b> 5 cm to 15 cm</li>
            <li><b>Orientation Azimuth:</b> -30° (East-South) to +30° (West-South)</li>
            <li><b>Glazing Area:</b> 1.0 m² to 3.5 m²</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

run_opt_btn = st.button("🚀 Run Multi-Objective Thermal Optimization", type="primary", use_container_width=True)

if run_opt_btn or "opt_results" in st.session_state:
    if run_opt_btn or "opt_results" not in st.session_state:
        with st.spinner("Searching parametric space and running multi-objective physics simulations..."):
            optimizer = ThermalOptimizer(mat_db)
            opt_res = optimizer.optimize_design(base_cfg, weather_df, target_indoor_temp=target_temp)
            st.session_state.opt_results = opt_res

    opt_res = st.session_state.opt_results
    best = opt_res['best_option']
    top_10 = opt_res['top_10_designs']
    all_res = opt_res['all_search_results']

    # ---------------------------------------------------------
    # BEST RECOMMENDED DESIGN HIGHLIGHT CARD
    # ---------------------------------------------------------
    st.subheader("🏆 Recommended Optimal Shelter Design")

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(15, 23, 42, 0.95) 100%); padding: 1.6rem; border-radius: 16px; border: 2px solid #10B981; margin-bottom: 1.5rem; box-shadow: 0 15px 35px rgba(16, 185, 129, 0.15);">
        <h3 style="color: #10B981; margin-top: 0;">🌟 Winner: {best['wall_material']} + {best['insulation_material']} ({best['insulation_thickness_cm']} cm)</h3>
        <p style="font-size: 1.05rem;">
            <b>Wall U-Value:</b> <code style="color:#00F0FF;">{best['wall_u_value']} W/m²K</code> | 
            <b>Azimuth Orientation:</b> <code>{best['orientation_deg']}° South</code> | 
            <b>Window Area:</b> <code>{best['window_area_m2']} m²</code>
        </p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 0.85rem; color: #94A3B8;">AVG INDOOR TEMP</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #F8FAFC;">{best['avg_indoor_temp']} °C</div>
            </div>
            <div>
                <div style="font-size: 0.85rem; color: #94A3B8;">MIN NIGHT TEMP</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #38BDF8;">{best['min_indoor_temp']} °C</div>
            </div>
            <div>
                <div style="font-size: 0.85rem; color: #94A3B8;">TOTAL HEAT LOSS</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #F59E0B;">{best['total_heat_loss_kwh']} kWh</div>
            </div>
            <div>
                <div style="font-size: 0.85rem; color: #94A3B8;">THERMAL EFFICIENCY</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #10B981;">{best['thermal_efficiency_pct']}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Apply Recommended Optimal Design to Active Shelter Settings 🛠️", type="secondary"):
        w_mat_info = mat_db.get_material_by_name(best['wall_material'])
        i_mat_info = mat_db.get_material_by_name(best['insulation_material'])
        st.session_state.wall_stack = mat_db.calculate_layer_stack([
            {"material_id": w_mat_info['id'], "thickness_m": 0.25},
            {"material_id": i_mat_info['id'], "thickness_m": best['insulation_thickness_cm'] / 100.0}
        ], "wall")
        st.session_state.shelter_config['window_area'] = float(best['window_area_m2'])
        st.session_state.shelter_config['orientation_deg'] = float(best['orientation_deg'])
        st.success("Applied optimal wall stack, orientation, and window area to active session config!")

    st.divider()

    # ---------------------------------------------------------
    # PARETO SEARCH SCATTER PLOT & TOP 10 TABLE
    # ---------------------------------------------------------
    st.subheader("📊 Optimization Search Space (Heat Loss vs Solar Gain vs Indoor Temp)")

    fig_scatter = px.scatter(
        all_res,
        x='total_heat_loss_kwh',
        y='total_solar_gain_kwh',
        size='thermal_efficiency_pct',
        color='avg_indoor_temp',
        hover_data=['wall_material', 'insulation_material', 'insulation_thickness_cm', 'orientation_deg'],
        color_continuous_scale='Viridis',
        labels={'total_heat_loss_kwh': 'Total Heat Loss (kWh)', 'total_solar_gain_kwh': 'Solar Heat Gain (kWh)', 'avg_indoor_temp': 'Avg Indoor Temp (°C)'}
    )

    fig_scatter.update_layout(
        height=480,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    st.subheader("🔝 Top 10 Pareto Optimal Shelter Designs")
    st.dataframe(top_10.drop(columns=['optimization_score']), use_container_width=True)
