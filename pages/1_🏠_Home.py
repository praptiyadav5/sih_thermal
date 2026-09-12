import streamlit as st
import numpy as np
import pandas as pd

from backend.session_state import ensure_session_state
from backend.ui_theme import (
    inject_custom_css,
    render_hero_banner,
    render_apogee_hero,
    render_animated_shelter_graphic,
)

try:
    st.set_page_config(page_title="Home | Thermal Shelter Simulation", page_icon="🏠", layout="wide")
except Exception:
    pass

ensure_session_state()
inject_custom_css()

# Safe access to shared session state
mat_db = st.session_state.get("mat_db")
weather_mgr = st.session_state.get("weather_mgr")
shelter_cfg = st.session_state.get("shelter_config", {})
location_name = st.session_state.get("location_name", "Leh, Ladakh, India")
material_count = len(mat_db.get_all_materials()) if mat_db is not None else 14

w_df = st.session_state.get("weather_df")
if w_df is not None and "temperature_c" in w_df.columns:
    amb_temp = f"{w_df['temperature_c'].min():.1f}"
    sol_peak = f"{w_df['solar_radiation_w_m2'].max():.0f}" if "solar_radiation_w_m2" in w_df.columns else "1,048"
else:
    amb_temp = "-16.2"
    sol_peak = "1,048"

# ---------------------------------------------------------
# 1. APOGEE MOTION HERO & DYNAMIC PHYSICS VISUALIZATION
# ---------------------------------------------------------
render_apogee_hero(
    location=location_name,
    temp_indoor="+18.4",
    temp_ambient=amb_temp,
    solar_peak=sol_peak
)

render_animated_shelter_graphic()

# ---------------------------------------------------------
# 2. QUICK STATS STRIP
# ---------------------------------------------------------
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Material Library</div>
        <div class="metric-value">{material_count}+</div>
        <div class="metric-sub">Verified thermal &amp; insulation materials</div>
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
        <div class="metric-sub">Any location via Open-Meteo Geo-API</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-title">Solver Architecture</div>
        <div class="metric-value">PyANSYS + FEA</div>
        <div class="metric-sub">APDL batch scripts + transient engine</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. INTERACTIVE THERMAL PHYSICS QUICK-LAB
# ---------------------------------------------------------
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom: 0.8rem; flex-wrap:wrap; gap:8px;">
    <div>
        <span style="font-size:0.75rem; font-weight:700; color:#38bdf8; letter-spacing:0.08em; text-transform:uppercase;">⚡ Live Simulation Sandbox</span>
        <h2 style="margin:0.2rem 0; font-size:1.65rem;">Thermal Physics Quick-Lab</h2>
        <p style="color:#94a3b8; font-size:0.95rem; margin:0;">Tweak key envelope and climate variables below to see instantaneous thermal delta and insulation impact before running a full transient mesh.</p>
    </div>
    <div>
        <span class="pulse-badge"><span class="apogee-live-dot"></span> Real-Time Conduction &amp; Solar Engine</span>
    </div>
</div>
""", unsafe_allow_html=True)

lab_col_left, lab_col_right = st.columns([1.1, 1])

QUICK_PRESETS = {
    "Leh, Ladakh, India (-16°C, High UV)": {"temp_min": -16.2, "solar": 1050, "lat": 34.15, "name": "Leh, Ladakh, India"},
    "Dras Valley, India (-35°C, Extreme Cold)": {"temp_min": -34.8, "solar": 920, "lat": 34.43, "name": "Dras, Kargil, India (Coldest Inhabited Place in India)"},
    "Reykjavik, Iceland (-5°C, Low Solar)": {"temp_min": -5.4, "solar": 480, "lat": 64.15, "name": "Reykjavik, Iceland"},
    "Zermatt, Swiss Alps (-22°C, Snow Gale)": {"temp_min": -22.0, "solar": 980, "lat": 46.02, "name": "Zermatt, Switzerland (Alps)"},
    "Nuuk, Greenland (-28°C, Polar Blizzard)": {"temp_min": -28.2, "solar": 380, "lat": 64.18, "name": "Nuuk, Greenland"},
    "Yellowknife, Canada (-30°C, Arctic Subsoil)": {"temp_min": -30.5, "solar": 520, "lat": 62.45, "name": "Yellowknife, Northwest Territories, Canada"},
}

with lab_col_left:
    st.markdown('<div class="glass-card" style="padding:1.4rem;">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#38bdf8;'>🎛️ Adjust Envelope Parameters</h4>", unsafe_allow_html=True)
    
    selected_quick_loc = st.selectbox(
        "Climate Region Preset",
        list(QUICK_PRESETS.keys()),
        index=0,
        key="quick_loc_select"
    )
    loc_meta = QUICK_PRESETS[selected_quick_loc]
    
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        quick_xps_thick_mm = st.slider("XPS Wall Insulation", 40, 260, 100, step=10, format="%d mm")
    with q_col2:
        quick_shape = st.selectbox("Roof Topology", ["Rectangular", "Gable", "Dome/Arch", "Monoslope"], index=1)
        
    q_col3, q_col4 = st.columns(2)
    with q_col3:
        quick_win_area = st.slider("South Glazing Area", 1.0, 6.0, 2.2, step=0.2, format="%.1f m²")
    with q_col4:
        quick_glazing_type = st.selectbox("Glazing Spec", ["Double Low-E (U=1.6)", "Triple Argon (U=0.8)", "Single Glaze (U=2.8)"], index=0)
    
    st.markdown('</div>', unsafe_allow_html=True)

k_mud = 0.75
t_mud = 0.25
r_mud = t_mud / k_mud

k_xps = 0.032
t_xps = quick_xps_thick_mm / 1000.0
r_xps = t_xps / k_xps

r_si = 0.13
r_se = 0.04
total_r_wall = r_si + r_mud + r_xps + r_se
wall_u = 1.0 / total_r_wall

win_u_val = 1.6 if "Double" in quick_glazing_type else (0.8 if "Triple" in quick_glazing_type else 2.8)
win_shgc_val = 0.60 if "Double" in quick_glazing_type else (0.50 if "Triple" in quick_glazing_type else 0.75)

ql_l, ql_w, ql_h = 6.0, 4.0, 2.4
wall_gross_area = 2 * (ql_l + ql_w) * ql_h
net_wall_area = max(10.0, wall_gross_area - quick_win_area - 2.0)
floor_area = ql_l * ql_w

ambient_cold = loc_meta["temp_min"]
solar_irrad = loc_meta["solar"]
daily_solar_kwh = (solar_irrad * quick_win_area * win_shgc_val * 6.5) / 1000.0
solar_watts_equiv = (daily_solar_kwh * 1000.0) / 24.0

total_ua = (net_wall_area * wall_u) + (floor_area * 0.25) + (floor_area * 0.35) + (quick_win_area * win_u_val) + (1.2 * 1005 * 0.5 * (ql_l * ql_w * ql_h) / 3600.0)
temp_rise = (solar_watts_equiv + 150.0) / total_ua
predicted_indoor_peak = ambient_cold + (temp_rise * 1.35)
savings_pct = min(96.0, max(50.0, (1.0 - (wall_u / 2.1)) * 100.0))

with lab_col_right:
    st.markdown('<div class="quick-lab-box">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#38bdf8; display:flex; justify-content:space-between;'><span>📊 Estimated Steady-State Response</span><span style='font-size:0.8rem; color:#94a3b8;'>Transient Bound</span></h4>", unsafe_allow_html=True)
    
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:0.9rem; margin-bottom:0.7rem;">
            <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Indoor Peak Temp</div>
            <div style="font-size:1.8rem; font-weight:800; color:#38bdf8; font-family:'JetBrains Mono', monospace;">+{predicted_indoor_peak:.1f}°C</div>
            <div style="font-size:0.75rem; color:#6ee7b7;">▲ +{predicted_indoor_peak - ambient_cold:.1f}°C over ambient ({ambient_cold:.1f}°C)</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:0.9rem; margin-bottom:0.7rem;">
            <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Composite Wall U-Value</div>
            <div style="font-size:1.8rem; font-weight:800; color:#f8fafc; font-family:'JetBrains Mono', monospace;">{wall_u:.2f} <span style="font-size:0.9rem; color:#94a3b8;">W/m²K</span></div>
            <div style="font-size:0.75rem; color:#94a3b8;">R-value: {total_r_wall:.2f} m²K/W ({quick_xps_thick_mm}mm XPS)</div>
        </div>
        """, unsafe_allow_html=True)

    m3, m4 = st.columns(2)
    with m3:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:0.9rem;">
            <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Daily Solar Capture</div>
            <div style="font-size:1.5rem; font-weight:800; color:#fbbf24; font-family:'JetBrains Mono', monospace;">{daily_solar_kwh:.1f} <span style="font-size:0.85rem;">kWh/day</span></div>
            <div style="font-size:0.75rem; color:#94a3b8;">Through {quick_win_area:.1f}m² south glazing</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:0.9rem;">
            <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase; font-weight:700;">Heating Energy Saved</div>
            <div style="font-size:1.5rem; font-weight:800; color:#34d399; font-family:'JetBrains Mono', monospace;">{savings_pct:.1f}%</div>
            <div style="font-size:0.75rem; color:#94a3b8;">vs uninsulated reference envelope</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Push Quick-Lab Settings to 3D Design & Simulation", type="primary", use_container_width=True):
        st.session_state.location_name = loc_meta["name"]
        st.session_state.shelter_config["shape"] = quick_shape
        st.session_state.shelter_config["window_area"] = quick_win_area
        st.session_state.shelter_config["window_u_value"] = win_u_val
        st.session_state.shelter_config["window_shgc"] = win_shgc_val
        st.session_state.wall_stack = mat_db.calculate_layer_stack([
            {"material_id": "mud_brick", "thickness_m": 0.25},
            {"material_id": "xps_insulation", "thickness_m": t_xps}
        ], "wall")
        st.toast(f"✅ Loaded {loc_meta['name']} with {quick_xps_thick_mm}mm XPS into session!", icon="❄️")
        st.switch_page("pages/2_📐_Shelter_Design.py")
        
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. CURATED COLD-CLIMATE ARCHITECTURAL ARCHETYPES
# ---------------------------------------------------------
st.markdown("""
<div>
    <span style="font-size:0.75rem; font-weight:700; color:#38bdf8; letter-spacing:0.08em; text-transform:uppercase;">🏛️ Proven Engineering Archetypes</span>
    <h2 style="margin:0.2rem 0; font-size:1.65rem;">Curated High-Altitude Shelter Designs</h2>
    <p style="color:#94a3b8; font-size:0.95rem; margin-bottom:1.2rem;">Click any architecture to instantly load its complete 3D geometry, material stack, and climate boundaries into your active workspace.</p>
</div>
""", unsafe_allow_html=True)

arch_col1, arch_col2, arch_col3, arch_col4 = st.columns(4)

with arch_col1:
    st.markdown("""
    <div class="archetype-card">
        <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                <span class="badge-pill" style="font-size:0.7rem;">Himalayan Plateau</span>
                <span style="font-size:1.2rem;">🏔️</span>
            </div>
            <h4 style="margin:0 0 0.4rem 0; color:#f8fafc; font-size:1.05rem;">Ladakhi Solar Trombe</h4>
            <p style="font-size:0.83rem; color:#94a3b8; line-height:1.45; margin-bottom:0.85rem;">
                High-mass 35cm sun-dried mud brick with 10cm external XPS. South glazing charges the internal masonry battery during peak sunlight.
            </p>
            <div style="display:flex; flex-wrap:wrap; gap:5px; margin-bottom:1rem;">
                <span class="spec-tag">R-4.2 m²K/W</span>
                <span class="spec-tag">3,524m Elev</span>
                <span class="spec-tag">Rectangular</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Load Ladakhi Trombe", key="btn_arch_1", use_container_width=True):
        st.session_state.location_name = "Leh, Ladakh, India"
        st.session_state.shelter_config["shape"] = "Rectangular"
        st.session_state.shelter_config["window_area"] = 2.4
        st.session_state.wall_stack = mat_db.calculate_layer_stack([
            {"material_id": "mud_brick", "thickness_m": 0.35},
            {"material_id": "xps_insulation", "thickness_m": 0.10}
        ], "wall")
        st.toast("Loaded Ladakhi Solar Trombe archetype!", icon="🏔️")
        st.rerun()

with arch_col2:
    st.markdown("""
    <div class="archetype-card">
        <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                <span class="badge-pill" style="font-size:0.7rem; background:rgba(56,189,248,0.15); border-color:#38bdf8;">Polar Arctic</span>
                <span style="font-size:1.2rem;">❄️</span>
            </div>
            <h4 style="margin:0 0 0.4rem 0; color:#f8fafc; font-size:1.05rem;">Arctic Monoslope Pod</h4>
            <p style="font-size:0.83rem; color:#94a3b8; line-height:1.45; margin-bottom:0.85rem;">
                15° wind-deflecting roof to shrug off 30 m/s polar gale winds. Vacuum Insulated Panels (VIP) with triple argon glazing.
            </p>
            <div style="display:flex; flex-wrap:wrap; gap:5px; margin-bottom:1rem;">
                <span class="spec-tag">R-7.5 m²K/W</span>
                <span class="spec-tag">-35°C Rated</span>
                <span class="spec-tag">Monoslope</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Load Arctic Pod", key="btn_arch_2", use_container_width=True):
        st.session_state.location_name = "Dras, Kargil, India (Coldest Inhabited Place in India)"
        st.session_state.shelter_config["shape"] = "Monoslope"
        st.session_state.shelter_config["window_area"] = 1.4
        st.session_state.shelter_config["window_u_value"] = 0.8
        st.session_state.wall_stack = mat_db.calculate_layer_stack([
            {"material_id": "ceb", "thickness_m": 0.15},
            {"material_id": "vip_panel", "thickness_m": 0.04}
        ], "wall")
        st.toast("Loaded Arctic Monoslope Pod archetype!", icon="❄️")
        st.rerun()

with arch_col3:
    st.markdown("""
    <div class="archetype-card">
        <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                <span class="badge-pill" style="font-size:0.7rem; background:rgba(16,185,129,0.15); border-color:#10b981;">Alpine Forest</span>
                <span style="font-size:1.2rem;">🌲</span>
            </div>
            <h4 style="margin:0 0 0.4rem 0; color:#f8fafc; font-size:1.05rem;">Alpine Timber Cabin</h4>
            <p style="font-size:0.83rem; color:#94a3b8; line-height:1.45; margin-bottom:0.85rem;">
                Cross-Laminated Timber (CLT) structural shell lined with breathable rock mineral wool. Steep 38° gable roof for natural snow-shedding.
            </p>
            <div style="display:flex; flex-wrap:wrap; gap:5px; margin-bottom:1rem;">
                <span class="spec-tag">R-4.8 m²K/W</span>
                <span class="spec-tag">Low Embodied C</span>
                <span class="spec-tag">Gable</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Load Alpine Cabin", key="btn_arch_3", use_container_width=True):
        st.session_state.location_name = "Zermatt, Switzerland (Alps)"
        st.session_state.shelter_config["shape"] = "Gable"
        st.session_state.shelter_config["window_area"] = 2.0
        st.session_state.wall_stack = mat_db.calculate_layer_stack([
            {"material_id": "timber_wood", "thickness_m": 0.10},
            {"material_id": "mineral_wool", "thickness_m": 0.12}
        ], "wall")
        st.toast("Loaded Alpine Timber Cabin archetype!", icon="🌲")
        st.rerun()

with arch_col4:
    st.markdown("""
    <div class="archetype-card">
        <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                <span class="badge-pill" style="font-size:0.7rem; background:rgba(245,158,11,0.15); border-color:#f59e0b;">Permafrost</span>
                <span style="font-size:1.2rem;">🧊</span>
            </div>
            <h4 style="margin:0 0 0.4rem 0; color:#f8fafc; font-size:1.05rem;">Permafrost Arch Vault</h4>
            <p style="font-size:0.83rem; color:#94a3b8; line-height:1.45; margin-bottom:0.85rem;">
                Curved aerodynamic vault on raised pilings. Prevents shelter heat from melting underlying sensitive frozen permafrost subsoil.
            </p>
            <div style="display:flex; flex-wrap:wrap; gap:5px; margin-bottom:1rem;">
                <span class="spec-tag">R-5.4 m²K/W</span>
                <span class="spec-tag">Thermal Stilt</span>
                <span class="spec-tag">Dome/Arch</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Load Arch Vault", key="btn_arch_4", use_container_width=True):
        st.session_state.location_name = "Yellowknife, Northwest Territories, Canada"
        st.session_state.shelter_config["shape"] = "Dome/Arch"
        st.session_state.shelter_config["window_area"] = 1.6
        st.session_state.wall_stack = mat_db.calculate_layer_stack([
            {"material_id": "pu_foam", "thickness_m": 0.12},
            {"material_id": "timber_wood", "thickness_m": 0.05}
        ], "wall")
        st.toast("Loaded Permafrost Arch Vault archetype!", icon="🧊")
        st.rerun()

st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. FIVE-STEP GUIDED ENGINEERING PIPELINE
# ---------------------------------------------------------
st.markdown("""
<div>
    <span style="font-size:0.75rem; font-weight:700; color:#38bdf8; letter-spacing:0.08em; text-transform:uppercase;">🗺️ Guided End-to-End Workflow</span>
    <h2 style="margin:0.2rem 0; font-size:1.65rem;">Five Stages of High-Altitude Engineering</h2>
    <p style="color:#94a3b8; font-size:0.95rem; margin-bottom:1.2rem;">Follow our systematic pipeline to transform site climate extremes into a zero-carbon, thermally stable architecture.</p>
</div>
""", unsafe_allow_html=True)

step_cols = st.columns(5)
steps = [
    ("1", "📐", "Design Studio", "Configure 3D dimensions, roof topology, and multi-layer wall, roof, and floor stacks.", "#38bdf8", "pages/2_📐_Shelter_Design.py", "Open Design ➔"),
    ("2", "🌤️", "Climate Engine", "Pull real Open-Meteo hourly irradiance, sub-zero temps, and gale wind velocities worldwide.", "#06b6d4", "pages/3_🌤️_Climate_Conditions.py", "Set Climate ➔"),
    ("3", "⚡", "Physics Solver", "Execute transient multi-layer conduction simulations or generate production PyANSYS APDL scripts.", "#f59e0b", "pages/4_⚡_Simulation.py", "Run Solver ➔"),
    ("4", "📊", "3D Heat Analytics", "Inspect hourly indoor vs outdoor temperature curves, component heat-loss breakdown, and 3D heatmaps.", "#10b981", "pages/5_📊_Results.py", "View Analytics ➔"),
    ("5", "🚀", "Optimization", "Run multi-objective Pareto searches across materials, insulation thickness, and orientation.", "#a855f7", "pages/7_🚀_Optimization.py", "Optimize ➔"),
]

for col, (num, icon, title, desc, color, page_path, btn_label) in zip(step_cols, steps):
    with col:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; height:100%; margin-bottom:0.6rem; border-top: 3px solid {color};">
            <div style="display:inline-flex; width:28px; height:28px; align-items:center; justify-content:center; border-radius:50%; background:rgba(255,255,255,0.06); font-size:0.75rem; font-weight:800; color:{color}; margin-bottom:0.4rem;">{num}</div>
            <div style="font-size:2rem; margin:0.2rem 0;">{icon}</div>
            <div style="font-weight:700; color:#F8FAFC; margin-bottom:0.4rem; font-size:1.02rem;">{title}</div>
            <div style="font-size:0.83rem; color:#94A3B8; line-height:1.45; min-height:65px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        try:
            st.page_link(page_path, label=btn_label, use_container_width=True)
        except Exception:
            st.page_link(page_path, label=btn_label)

st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. THE EXTREME COLD CHALLENGE VS PASSIVE SOLUTIONS
# ---------------------------------------------------------
col_problem, col_objective = st.columns([1.3, 1])

with col_problem:
    st.markdown("""
    <div class="glass-card" style="height:100%; border-left: 4px solid #38bdf8;">
        <h3 style="color: #38bdf8; margin-top: 0; display:flex; align-items:center; gap:8px;">
            <span>🏔️</span> The High-Altitude Extreme Cold Challenge
        </h3>
        <p style="font-size: 0.98rem; line-height: 1.65; color: #CBD5E1;">
            High-altitude regions like <b>Ladakh (Leh, Dras, Nyoma, Pangong)</b>, the Arctic tundra, and alpine summits
            combine harsh weather conditions that cause standard shelters to fail rapidly:
        </p>
        <ul style="color:#CBD5E1; line-height:1.8; font-size:0.92rem;">
            <li><b>Severe Sub-Zero Cold:</b> Ambient winter temperatures drop to <b>-16°C in Leh</b> and plummet below <b>-35°C in Dras</b>.</li>
            <li><b>Intense High-Altitude Radiation:</b> Thin mountain atmosphere delivers clear-sky solar irradiance exceeding <b>1,050 W/m²</b>.</li>
            <li><b>Forced Convective Gale Winds:</b> Mountain winds of 10–25 m/s strip heat from uninsulated envelope skins.</li>
            <li><b>Subsoil Permafrost:</b> Frozen ground (-8°C) creates a persistent conductive thermal sink beneath foundations.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_objective:
    st.markdown("""
    <div class="glass-card" style="height:100%; border-left: 4px solid #10B981;">
        <h3 style="color: #10B981; margin-top: 0; display:flex; align-items:center; gap:8px;">
            <span>🎯</span> Passive Physics Design Philosophy
        </h3>
        <p style="font-size: 0.98rem; line-height: 1.65; color: #CBD5E1;">
            Traditional active heating burns scarce fossil fuels and emits carbon. Our studio empowers engineers to achieve <b>zero-carbon thermal comfort</b> passively:
        </p>
        <ul style="color:#CBD5E1; line-height:1.8; font-size:0.92rem;">
            <li><b>Diurnal Heat Storage:</b> High-capacity thermal mass (mud brick, stone, concrete) absorbs daytime sun and emits heat all night.</li>
            <li><b>Super-Insulated Envelope:</b> Multi-layer XPS, EPS, and VIP composites reduce envelope conductance (U &lt; 0.22 W/m²K).</li>
            <li><b>Orientation Geometry:</b> Precise azimuth and roof pitch maximize solar incidence while deflecting prevailing winds.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. ACTIVE SESSION SNAPSHOT & QUICK ACTIONS
# ---------------------------------------------------------
with st.expander("📍 Active Workspace Snapshot & Loaded Parameters", expanded=False):
    snap1, snap2, snap3, snap4 = st.columns(4)
    snap1.metric("Current Location", location_name)
    snap2.metric("Selected Shape", shelter_cfg.get("shape", "Rectangular"))
    dims_str = f"{shelter_cfg.get('length', 6.0)}m × {shelter_cfg.get('width', 4.0)}m × {shelter_cfg.get('height', 2.4)}m"
    snap3.metric("Shelter Dimensions", dims_str)
    cur_u = st.session_state.get("wall_stack", {}).get("U_value", 0.28)
    snap4.metric("Active Wall U-Value", f"{cur_u:.2f} W/m²K")
    st.caption("All parameters sync automatically across Design, Climate, Simulation, Comparison, and Optimization studios.")

st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 8. CALL TO ACTION FOOTER
# ---------------------------------------------------------
st.markdown("""
<div class="glass-card" style="text-align:center; padding: 2.2rem; background: linear-gradient(135deg, rgba(15,23,42,0.92) 0%, rgba(30,58,138,0.3) 100%);">
    <h3 style="margin-top:0; color:#F8FAFC; font-size:1.5rem;">Ready to engineer your cold-climate shelter?</h3>
    <p style="color:#94A3B8; font-size:0.98rem; max-width:680px; margin:0.4rem auto 1.2rem auto; line-height:1.6;">
        Jump straight into the 3D parametric CAD studio to adjust dimensions and wall assemblies,
        or benchmark multiple material combinations under identical sub-zero weather conditions.
    </p>
</div>
""", unsafe_allow_html=True)

cta1, cta2 = st.columns(2)
with cta1:
    if st.button("🚀 Open 3D Parametric CAD Studio", type="primary", use_container_width=True):
        st.switch_page("pages/2_📐_Shelter_Design.py")
with cta2:
    if st.button("⚖️ Compare Materials & Shapes Side-by-Side", use_container_width=True):
        st.switch_page("pages/6_⚖️_Comparison.py")
