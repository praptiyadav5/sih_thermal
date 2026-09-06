import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from backend.materials import MaterialDatabase
from backend.simulation import ThermalSimulationEngine
from backend.ui_theme import inject_custom_css, render_hero_banner

st.set_page_config(page_title="Comparison | Thermal Shelter", page_icon="⚖️", layout="wide")
inject_custom_css()

mat_db = st.session_state.mat_db
sim_engine = st.session_state.sim_engine
weather_df = st.session_state.weather_df
base_cfg = st.session_state.shelter_config

render_hero_banner(
    title="⚖️ Multi-Design & Material Comparative Benchmark Studio",
    subtitle="Benchmarking traditional mud brick, stone masonry, XPS insulated frames, and VIP panels under identical climate boundary conditions.",
    badge_text="Comparison Studio"
)

tab_presets, tab_custom = st.tabs([
    "📌 Design Preset Comparison",
    "🔬 Custom Material & Shape Comparison"
])

# ===========================================================
# TAB 1: ORIGINAL PRESET DESIGN COMPARISON (UNCHANGED)
# ===========================================================
with tab_presets:
    PRESET_DESIGNS = {
        "Design A: Traditional Mud Brick (Trombe Wall)": {
            "wall_layers": [{"material_id": "mud_brick", "thickness_m": 0.35}],
            "roof_layers": [{"material_id": "timber_wood", "thickness_m": 0.08}],
            "floor_layers": [{"material_id": "concrete", "thickness_m": 0.15}],
            "win_u": 2.8, "win_shgc": 0.70, "win_area": 2.0, "desc": "High thermal mass sun-dried mud brick wall (0.35m) with single glazing."
        },
        "Design B: Local Granite Stone + EPS Insulation": {
            "wall_layers": [{"material_id": "stone_masonry", "thickness_m": 0.25}, {"material_id": "eps_insulation", "thickness_m": 0.06}],
            "roof_layers": [{"material_id": "eps_insulation", "thickness_m": 0.08}, {"material_id": "metal_sheet", "thickness_m": 0.002}],
            "floor_layers": [{"material_id": "concrete", "thickness_m": 0.15}, {"material_id": "eps_insulation", "thickness_m": 0.04}],
            "win_u": 1.8, "win_shgc": 0.62, "win_area": 1.8, "desc": "Abundant local granite stone masonry lined with 6cm EPS insulation."
        },
        "Design C: XPS Insulated Timber Composite": {
            "wall_layers": [{"material_id": "timber_wood", "thickness_m": 0.04}, {"material_id": "xps_insulation", "thickness_m": 0.10}],
            "roof_layers": [{"material_id": "pu_foam", "thickness_m": 0.10}, {"material_id": "timber_wood", "thickness_m": 0.04}],
            "floor_layers": [{"material_id": "concrete", "thickness_m": 0.15}, {"material_id": "xps_insulation", "thickness_m": 0.08}],
            "win_u": 1.4, "win_shgc": 0.60, "win_area": 1.6, "desc": "Lightweight timber composite structure with 10cm extruded polystyrene (XPS)."
        },
        "Design D: Advanced Vacuum Insulated Panel (VIP)": {
            "wall_layers": [{"material_id": "ceb", "thickness_m": 0.15}, {"material_id": "vip_panel", "thickness_m": 0.03}],
            "roof_layers": [{"material_id": "vip_panel", "thickness_m": 0.03}, {"material_id": "pu_foam", "thickness_m": 0.08}],
            "floor_layers": [{"material_id": "concrete", "thickness_m": 0.15}, {"material_id": "xps_insulation", "thickness_m": 0.10}],
            "win_u": 0.8, "win_shgc": 0.50, "win_area": 1.5, "desc": "Ultra-thin 3cm Vacuum Insulated Panel (VIP) combined with triple-pane glazing."
        }
    }

    st.subheader("⚙️ Selected Benchmark Cases")

    selected_preset_keys = st.multiselect(
        "Select designs to compare:",
        list(PRESET_DESIGNS.keys()),
        default=list(PRESET_DESIGNS.keys())
    )

    if len(selected_preset_keys) < 2:
        st.warning("Please select at least 2 designs to compare.")
    else:
        benchmark_results = {}

        for key in selected_preset_keys:
            item = PRESET_DESIGNS[key]
            w_stack = mat_db.calculate_layer_stack(item["wall_layers"], "wall")
            r_stack = mat_db.calculate_layer_stack(item["roof_layers"], "roof")
            f_stack = mat_db.calculate_layer_stack(item["floor_layers"], "floor")

            cfg = dict(base_cfg)
            cfg['window_u_value'] = item['win_u']
            cfg['window_shgc'] = item['win_shgc']
            cfg['window_area'] = item['win_area']

            sim_res = sim_engine.run_simulation(cfg, weather_df, w_stack, r_stack, f_stack)
            benchmark_results[key] = {
                "config": item,
                "wall_stack": w_stack,
                "results": sim_res
            }

        st.divider()

        # ---------------------------------------------------------
        # COMPARATIVE KPI SUMMARY CARDS
        # ---------------------------------------------------------
        st.subheader("📊 Comparative Performance Summary")

        cols = st.columns(len(selected_preset_keys))
        colors = ["#EF4444", "#F59E0B", "#10B981", "#00F0FF"]

        summary_data = []

        for idx, (key, data) in enumerate(benchmark_results.items()):
            kpis = data['results']['kpis']
            w_stack = data['wall_stack']
            short_name = key.split(":")[0]

            summary_data.append({
                "Design": short_name,
                "Full Name": key,
                "Wall U-Value (W/m²K)": round(w_stack['u_value'], 3),
                "Avg Indoor Temp (°C)": round(kpis['avg_indoor_temp'], 1),
                "Min Indoor Temp (°C)": round(kpis['min_indoor_temp'], 1),
                "Total Heat Loss (kWh)": round(kpis['total_heat_loss_kwh'], 2),
                "Solar Heat Gain (kWh)": round(kpis['total_solar_gain_kwh'], 2),
                "Thermal Efficiency (%)": round(kpis['thermal_efficiency_pct'], 1)
            })

            with cols[idx]:
                st.markdown(f"""
                <div class="glass-card" style="border-top: 4px solid {colors[idx % len(colors)]};">
                    <h4 style="margin-top:0; font-size:1rem; color:{colors[idx % len(colors)]};">{short_name}</h4>
                    <p style="font-size:0.8rem; color:#94A3B8;">{key.split(':')[1]}</p>
                    <p><b>Wall U:</b> <code>{w_stack['u_value']:.3f} W/m²K</code></p>
                    <p><b>Avg Temp:</b> <span style="font-size:1.3rem; font-weight:700; color:#F8FAFC;">{kpis['avg_indoor_temp']:.1f} °C</span></p>
                    <p><b>Heat Loss:</b> {kpis['total_heat_loss_kwh']:.2f} kWh</p>
                    <p><b>Efficiency:</b> <span style="color:#10B981; font-weight:700;">{kpis['thermal_efficiency_pct']:.1f}%</span></p>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # ---------------------------------------------------------
        # COMPARATIVE CHARTS
        # ---------------------------------------------------------
        st.subheader("📈 Temperature Trajectory Comparison (°C)")

        fig_comp_temp = go.Figure()
        fig_comp_temp.add_trace(go.Scatter(x=weather_df['time'], y=weather_df['temperature_c'], mode='lines', name='Outdoor Ambient Temp', line=dict(color='#64748B', width=2, dash='dot')))

        for idx, (key, data) in enumerate(benchmark_results.items()):
            df_ts = data['results']['time_series']
            fig_comp_temp.add_trace(go.Scatter(
                x=df_ts['time'],
                y=df_ts['indoor_temp'],
                mode='lines+markers',
                name=key.split(":")[0],
                line=dict(color=colors[idx % len(colors)], width=3)
            ))

        fig_comp_temp.add_hrect(
            y0=18.0, y1=24.0, fillcolor="rgba(16, 185, 129, 0.12)", line_width=0,
            annotation_text="Thermal Comfort Zone (18°C+)",
            annotation_font=dict(color="#34D399", size=12)
        )

        fig_comp_temp.update_layout(
            height=450,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
            yaxis_title="Indoor Temperature (°C)",
            xaxis_title="Time / Hour",
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(fig_comp_temp, use_container_width=True)

        st.divider()

        col_b1, col_b2 = st.columns([1, 1])

        with col_b1:
            st.subheader("🔥 Total Heat Loss Comparison (kWh)")
            df_sum = pd.DataFrame(summary_data)
            fig_bar_loss = px.bar(
                df_sum,
                x='Design',
                y='Total Heat Loss (kWh)',
                color='Design',
                text='Total Heat Loss (kWh)',
                color_discrete_sequence=colors
            )
            fig_bar_loss.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=12))
            fig_bar_loss.update_layout(
                height=380,
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.5)",
                font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
                showlegend=False
            )
            st.plotly_chart(fig_bar_loss, use_container_width=True)

        with col_b2:
            st.subheader("🏆 Thermal Efficiency Ranking (%)")
            df_sum_sorted = df_sum.sort_values(by="Thermal Efficiency (%)", ascending=False)
            fig_bar_eff = px.bar(
                df_sum_sorted,
                x='Thermal Efficiency (%)',
                y='Design',
                orientation='h',
                color='Thermal Efficiency (%)',
                color_continuous_scale='Viridis',
                text='Thermal Efficiency (%)'
            )
            fig_bar_eff.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=12))
            fig_bar_eff.update_layout(
                height=380,
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.5)",
                font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
                coloraxis_colorbar=dict(tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0"))
            )
            st.plotly_chart(fig_bar_eff, use_container_width=True)

        st.divider()

        # Ranking Data Table
        st.subheader("📋 Comprehensive Benchmarking Table")
        st.dataframe(df_sum.drop(columns=['Full Name']), use_container_width=True)

# ===========================================================
# TAB 2: CUSTOM MATERIAL & SHAPE COMPARISON (NEW)
# ===========================================================
with tab_custom:
    st.subheader("🔬 Build Your Own Comparison")
    st.caption(
        "Pick the shape and construction materials for each case yourself, then compare thermal performance "
        "side-by-side under the same climate and geometry conditions as your active shelter configuration."
    )

    shape_options = ["Rectangular", "Gable", "Dome/Arch", "Monoslope"]
    mat_names = mat_db.get_material_names()
    custom_colors = ["#A855F7", "#38BDF8", "#F97316", "#22C55E"]

    n_cases = st.number_input("Number of cases to compare", min_value=2, max_value=4, value=3, step=1, key="cc_num_cases")

    default_wall_idx = 0
    default_roof_idx = min(6, len(mat_names) - 1)
    default_floor_idx = min(3, len(mat_names) - 1)

    case_cols = st.columns(n_cases)
    case_inputs = []

    for i in range(n_cases):
        with case_cols[i]:
            st.markdown(f"""
            <div class="glass-card" style="border-top: 4px solid {custom_colors[i % len(custom_colors)]}; padding-top:0.8rem;">
                <h4 style="margin-top:0.6rem; color:{custom_colors[i % len(custom_colors)]};">Case {i+1}</h4>
            </div>
            """, unsafe_allow_html=True)

            c_name = st.text_input("Case name", value=f"Case {i+1}", key=f"cc_name_{i}")
            c_shape = st.selectbox("Shelter shape", shape_options, index=i % len(shape_options), key=f"cc_shape_{i}")

            st.markdown("**Wall**")
            c_wall_mat = st.selectbox("Wall material", mat_names, index=default_wall_idx, key=f"cc_wall_mat_{i}")
            c_wall_thick = st.number_input("Wall thickness (m)", min_value=0.05, max_value=0.50, value=0.25, step=0.01, format="%.2f", key=f"cc_wall_thick_{i}")

            st.markdown("**Roof**")
            c_roof_mat = st.selectbox("Roof material", mat_names, index=default_roof_idx, key=f"cc_roof_mat_{i}")
            c_roof_thick = st.number_input("Roof thickness (m)", min_value=0.02, max_value=0.30, value=0.10, step=0.01, format="%.2f", key=f"cc_roof_thick_{i}")

            st.markdown("**Floor**")
            c_floor_mat = st.selectbox("Floor material", mat_names, index=default_floor_idx, key=f"cc_floor_mat_{i}")
            c_floor_thick = st.number_input("Floor thickness (m)", min_value=0.05, max_value=0.30, value=0.15, step=0.01, format="%.2f", key=f"cc_floor_thick_{i}")

            case_inputs.append({
                "name": c_name.strip() if c_name.strip() else f"Case {i+1}",
                "shape": c_shape,
                "wall_mat": c_wall_mat, "wall_thick": c_wall_thick,
                "roof_mat": c_roof_mat, "roof_thick": c_roof_thick,
                "floor_mat": c_floor_mat, "floor_thick": c_floor_thick,
            })

    # Ensure display names are unique even if user types duplicates
    seen_names = {}
    for case in case_inputs:
        base_name = case["name"]
        if base_name in seen_names:
            seen_names[base_name] += 1
            case["name"] = f"{base_name} ({seen_names[base_name]})"
        else:
            seen_names[base_name] = 1

    st.divider()

    # ---------------------------------------------------------
    # RUN SIMULATIONS FOR EACH CUSTOM CASE
    # ---------------------------------------------------------
    custom_results = []

    for case in case_inputs:
        wall_info = mat_db.get_material_by_name(case["wall_mat"]) or mat_db.get_material_by_id("mud_brick")
        roof_info = mat_db.get_material_by_name(case["roof_mat"]) or mat_db.get_material_by_id("pu_foam")
        floor_info = mat_db.get_material_by_name(case["floor_mat"]) or mat_db.get_material_by_id("concrete")

        w_stack = mat_db.calculate_layer_stack([{"material_id": wall_info["id"], "thickness_m": case["wall_thick"]}], "wall")
        r_stack = mat_db.calculate_layer_stack([{"material_id": roof_info["id"], "thickness_m": case["roof_thick"]}], "roof")
        f_stack = mat_db.calculate_layer_stack([{"material_id": floor_info["id"], "thickness_m": case["floor_thick"]}], "floor")

        cfg = dict(base_cfg)
        cfg["shape"] = case["shape"]

        sim_res = sim_engine.run_simulation(cfg, weather_df, w_stack, r_stack, f_stack)
        custom_results.append({
            "name": case["name"],
            "case": case,
            "wall_stack": w_stack,
            "results": sim_res
        })

    # ---------------------------------------------------------
    # KPI SUMMARY CARDS
    # ---------------------------------------------------------
    st.subheader("📊 Custom Case Performance Summary")

    cols_c = st.columns(len(custom_results))
    custom_summary = []

    for idx, entry in enumerate(custom_results):
        kpis = entry["results"]["kpis"]
        w_stack = entry["wall_stack"]
        case = entry["case"]

        custom_summary.append({
            "Case": entry["name"],
            "Shape": case["shape"],
            "Wall Material": case["wall_mat"],
            "Roof Material": case["roof_mat"],
            "Floor Material": case["floor_mat"],
            "Wall U-Value (W/m²K)": round(w_stack["u_value"], 3),
            "Avg Indoor Temp (°C)": round(kpis["avg_indoor_temp"], 1),
            "Min Indoor Temp (°C)": round(kpis["min_indoor_temp"], 1),
            "Total Heat Loss (kWh)": round(kpis["total_heat_loss_kwh"], 2),
            "Solar Heat Gain (kWh)": round(kpis["total_solar_gain_kwh"], 2),
            "Thermal Efficiency (%)": round(kpis["thermal_efficiency_pct"], 1)
        })

        with cols_c[idx]:
            st.markdown(f"""
            <div class="glass-card" style="border-top: 4px solid {custom_colors[idx % len(custom_colors)]};">
                <h4 style="margin-top:0; font-size:1rem; color:{custom_colors[idx % len(custom_colors)]};">{entry['name']}</h4>
                <p style="font-size:0.8rem; color:#94A3B8;">{case['shape']} · {case['wall_mat']}</p>
                <p><b>Wall U:</b> <code>{w_stack['u_value']:.3f} W/m²K</code></p>
                <p><b>Avg Temp:</b> <span style="font-size:1.3rem; font-weight:700; color:#F8FAFC;">{kpis['avg_indoor_temp']:.1f} °C</span></p>
                <p><b>Heat Loss:</b> {kpis['total_heat_loss_kwh']:.2f} kWh</p>
                <p><b>Efficiency:</b> <span style="color:#10B981; font-weight:700;">{kpis['thermal_efficiency_pct']:.1f}%</span></p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ---------------------------------------------------------
    # TEMPERATURE TRAJECTORY CHART
    # ---------------------------------------------------------
    st.subheader("📈 Temperature Trajectory Comparison (°C)")

    fig_ct = go.Figure()
    fig_ct.add_trace(go.Scatter(
        x=weather_df["time"], y=weather_df["temperature_c"], mode="lines",
        name="Outdoor Ambient Temp", line=dict(color="#64748B", width=2, dash="dot")
    ))

    for idx, entry in enumerate(custom_results):
        df_ts = entry["results"]["time_series"]
        fig_ct.add_trace(go.Scatter(
            x=df_ts["time"], y=df_ts["indoor_temp"], mode="lines+markers",
            name=entry["name"], line=dict(color=custom_colors[idx % len(custom_colors)], width=3)
        ))

    fig_ct.add_hrect(
        y0=18.0, y1=24.0, fillcolor="rgba(16, 185, 129, 0.12)", line_width=0,
        annotation_text="Thermal Comfort Zone (18°C+)",
        annotation_font=dict(color="#34D399", size=12)
    )
    fig_ct.update_layout(
        height=450,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.5)",
        font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
        yaxis_title="Indoor Temperature (°C)",
        xaxis_title="Time / Hour",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_ct, use_container_width=True)

    st.divider()

    # ---------------------------------------------------------
    # BAR CHARTS
    # ---------------------------------------------------------
    col_cc1, col_cc2 = st.columns([1, 1])

    df_csum = pd.DataFrame(custom_summary)

    with col_cc1:
        st.subheader("🔥 Total Heat Loss Comparison (kWh)")
        fig_cbar_loss = px.bar(
            df_csum, x="Case", y="Total Heat Loss (kWh)", color="Case",
            text="Total Heat Loss (kWh)", color_discrete_sequence=custom_colors
        )
        fig_cbar_loss.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=12))
        fig_cbar_loss.update_layout(
            height=380, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
            showlegend=False
        )
        st.plotly_chart(fig_cbar_loss, use_container_width=True)

    with col_cc2:
        st.subheader("🏆 Thermal Efficiency Ranking (%)")
        df_csum_sorted = df_csum.sort_values(by="Thermal Efficiency (%)", ascending=False)
        fig_cbar_eff = px.bar(
            df_csum_sorted, x="Thermal Efficiency (%)", y="Case", orientation="h",
            color="Thermal Efficiency (%)", color_continuous_scale="Viridis", text="Thermal Efficiency (%)"
        )
        fig_cbar_eff.update_traces(textposition='outside', textfont=dict(color='#F8FAFC', size=12))
        fig_cbar_eff.update_layout(
            height=380, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
            coloraxis_colorbar=dict(tickfont=dict(color="#E2E8F0"), title_font=dict(color="#E2E8F0"))
        )
        st.plotly_chart(fig_cbar_eff, use_container_width=True)

    st.divider()

    st.subheader("📋 Custom Comparison Table")
    st.dataframe(df_csum, use_container_width=True)

st.divider()

col_nav1, col_nav2 = st.columns([3, 1])
with col_nav2:
    if st.button("Next: Automated Optimization 🚀", type="primary", use_container_width=True):
        st.switch_page("pages/7_🚀_Optimization.py")
