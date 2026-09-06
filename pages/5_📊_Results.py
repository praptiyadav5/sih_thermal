import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from backend.ui_theme import inject_custom_css, render_hero_banner

st.set_page_config(page_title="Results | Thermal Shelter", page_icon="📊", layout="wide")
inject_custom_css()

render_hero_banner(
    title="📊 Thermal Simulation Results Dashboard",
    subtitle="Hourly indoor temperature trajectory, component heat loss breakdown, heat flux vectors, and 3D spatial thermal heatmaps.",
    badge_text="Results Dashboard"
)

if st.session_state.simulation_results is None:
    st.warning("⚠️ No simulation results found in memory. Please run a simulation first in the Simulation tab.")
    if st.button("Go to Simulation Page ⚡"):
        st.switch_page("pages/4_⚡_Simulation.py")
    st.stop()

res = st.session_state.simulation_results
kpis = res['kpis']
df_ts = res['time_series']
comp_kwh = res['component_breakdown_kwh']

# Solver Mode Indicator Banner
if "LIVE" in res['solver_mode']:
    st.markdown('<span class="badge-ansys">🟢 LIVE ANSYS MECHANICAL SOLVER</span>', unsafe_allow_html=True)
else:
    st.markdown('<span class="badge-mock">🟡 MOCK / PHYSICS FALLBACK ENGINE</span>', unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# KPI METRIC CARDS
# ---------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Avg Indoor Temp</div>
        <div class="metric-value">{kpis['avg_indoor_temp']:.1f} °C</div>
        <div class="metric-sub">+{kpis['avg_indoor_temp'] - kpis['avg_outdoor_temp']:.1f}° vs Outdoor</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Min Indoor Temp</div>
        <div class="metric-value">{kpis['min_indoor_temp']:.1f} °C</div>
        <div class="metric-sub" style="color:#FF4B4B;">Night Peak Cold</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Solar Gain</div>
        <div class="metric-value">{kpis['total_solar_gain_kwh']:.2f}</div>
        <div class="metric-sub" style="color:#FF8F00;">kWh / Day</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Total Heat Loss</div>
        <div class="metric-value">{kpis['total_heat_loss_kwh']:.2f}</div>
        <div class="metric-sub" style="color:#EF4444;">kWh Envelope Loss</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Thermal Efficiency</div>
        <div class="metric-value">{kpis['thermal_efficiency_pct']:.1f}%</div>
        <div class="metric-sub" style="color:#10B981;">vs Uninsulated</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# TIME-SERIES GRAPHS
# ---------------------------------------------------------
st.subheader("📈 Indoor vs Outdoor Temperature Trajectory Over Time")

fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=df_ts['time'], y=df_ts['indoor_temp'], mode='lines+markers', name='Predicted Indoor Temp (°C)', line=dict(color='#00F0FF', width=3)))
fig_temp.add_trace(go.Scatter(x=df_ts['time'], y=df_ts['outdoor_temp'], mode='lines', name='Outdoor Ambient Temp (°C)', line=dict(color='#FF4B4B', width=2, dash='dash')))

fig_temp.add_hrect(
    y0=18.0, y1=24.0, fillcolor="rgba(16, 185, 129, 0.15)", line_width=0,
    annotation_text="Thermal Comfort Zone (18-24°C)", annotation_position="top left",
    annotation_font=dict(color="#34D399", size=12)
)

fig_temp.update_layout(
    height=420,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15, 23, 42, 0.5)",
    font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
    yaxis_title="Temperature (°C)",
    xaxis_title="Time / Hour",
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig_temp, use_container_width=True)

st.divider()

# Heat Loss Breakdown & Solar Gain Comparison
col_g1, col_g2 = st.columns([1, 1])

with col_g1:
    st.subheader("🔥 Hourly Component Heat Loss Breakdown (W)")
    fig_loss = go.Figure()
    fig_loss.add_trace(go.Scatter(x=df_ts['time'], y=df_ts['loss_wall_w'], stackgroup='one', name='Walls', line=dict(color='#3B82F6')))
    fig_loss.add_trace(go.Scatter(x=df_ts['time'], y=df_ts['loss_roof_w'], stackgroup='one', name='Roof', line=dict(color='#8B5CF6')))
    fig_loss.add_trace(go.Scatter(x=df_ts['time'], y=df_ts['loss_floor_w'], stackgroup='one', name='Floor', line=dict(color='#10B981')))
    fig_loss.add_trace(go.Scatter(x=df_ts['time'], y=df_ts['loss_win_w'], stackgroup='one', name='Windows', line=dict(color='#F59E0B')))
    fig_loss.add_trace(go.Scatter(x=df_ts['time'], y=df_ts['loss_door_w'], stackgroup='one', name='Doors', line=dict(color='#EF4444')))
    fig_loss.add_trace(go.Scatter(x=df_ts['time'], y=df_ts['loss_inf_w'], stackgroup='one', name='Infiltration', line=dict(color='#64748B')))

    fig_loss.update_layout(
        height=380,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
        yaxis_title="Heat Loss Rate (Watts)",
        xaxis_title="Time / Hour",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_loss, use_container_width=True)

with col_g2:
    st.subheader("🥧 Cumulative Heat Loss Contribution by Component")
    df_pie = pd.DataFrame({
        "Component": list(comp_kwh.keys()),
        "Heat Loss (kWh)": list(comp_kwh.values())
    })
    fig_pie = px.pie(
        df_pie,
        values='Heat Loss (kWh)',
        names='Component',
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_traces(textfont=dict(color='#0B1120', size=12))
    fig_pie.update_layout(
        height=380,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
        legend=dict(font=dict(color="#E2E8F0")),
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# SPATIAL 3D THERMAL DISTRIBUTION HEATMAP
# ---------------------------------------------------------
st.subheader("🧊 3D Spatial Indoor Temperature Distribution Surface Heatmap")
st.caption("Visualizes thermal gradient distribution across internal shelter coordinates (x, y, z).")

spatial = res['spatial_grid']
x, y, z = spatial['x'], spatial['y'], spatial['z']
T_grid = spatial['T_grid']

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

fig_3d = go.Figure(data=go.Volume(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=T_grid.flatten(),
    isomin=float(np.min(T_grid)),
    isomax=float(np.max(T_grid)),
    opacity=0.15,
    surface_count=8,
    colorscale='Thermal'
))

fig_3d.update_layout(
    scene=dict(
        xaxis_title='Length X (m)',
        yaxis_title='Width Y (m)',
        zaxis_title='Height Z (m)',
        aspectmode='data'
    ),
    height=550,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
    coloraxis_colorbar=dict(tickfont=dict(color="#E2E8F0")),
    margin=dict(l=10, r=10, t=30, b=10)
)

st.plotly_chart(fig_3d, use_container_width=True)

st.divider()

# Export Buttons
st.subheader("📥 Export Simulation Data")
col_d1, col_d2 = st.columns(2)
with col_d1:
    csv_data = df_ts.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Hourly Thermal Results (CSV)",
        data=csv_data,
        file_name="thermal_shelter_simulation_results.csv",
        mime="text/csv",
        use_container_width=True
    )
with col_d2:
    if st.button("Next: Compare Designs & Materials ⚖️", type="primary", use_container_width=True):
        st.switch_page("pages/6_⚖️_Comparison.py")
