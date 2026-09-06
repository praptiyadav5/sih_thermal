import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from backend.materials import MaterialDatabase
from backend.cad_geometry import generate_shelter_3d_cad_figure
from backend.ui_theme import inject_custom_css, render_hero_banner

st.set_page_config(page_title="Shelter Design | Thermal Shelter", page_icon="📐", layout="wide")
inject_custom_css()

mat_db = st.session_state.mat_db

render_hero_banner(
    title="📐 Shelter Parametric Design & CAD Studio",
    subtitle="Interactive 3D CAD schematic wireframe, azimuth orientation compass, and multi-layer wall, roof, and floor assemblies.",
    badge_text="CAD Studio"
)

# Tabbed Navigation inside page
tab_geom, tab_wall, tab_roof, tab_floor, tab_custom = st.tabs([
    "📐 Geometry & 3D CAD Preview",
    "🧱 Wall Construction Stack",
    "🏠 Roof Assembly",
    "🦶 Floor Assembly",
    "➕ Add Custom Material"
])

# ---------------------------------------------------------
# TAB 1: GEOMETRY & 3D CAD PREVIEW
# ---------------------------------------------------------
with tab_geom:
    st.subheader("Parametric Building Geometry & Interactive 3D CAD Schematics")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Bounding Box & Roof Control")
        cur_l = float(st.session_state.shelter_config.get("length", 6.0))
        cur_w = float(st.session_state.shelter_config.get("width", 4.0))
        cur_h = float(st.session_state.shelter_config.get("height", 2.4))
        cur_shape = st.session_state.shelter_config.get("shape", "Rectangular")

        st.session_state.shelter_config["length"] = st.number_input(
            "Shelter Length (m)", min_value=3.0, max_value=15.0, value=min(max(3.0, cur_l), 15.0), step=0.5, format="%.1f"
        )
        st.session_state.shelter_config["width"] = st.number_input(
            "Shelter Width (m)", min_value=2.5, max_value=10.0, value=min(max(2.5, cur_w), 10.0), step=0.5, format="%.1f"
        )
        st.session_state.shelter_config["height"] = st.number_input(
            "Eave Height (m)", min_value=1.8, max_value=5.0, value=min(max(1.8, cur_h), 5.0), step=0.1, format="%.1f"
        )
        
        shapes_list = ["Rectangular", "Gable", "Dome/Arch", "Monoslope"]
        shape_idx = shapes_list.index(cur_shape) if cur_shape in shapes_list else 0
        st.session_state.shelter_config["shape"] = st.selectbox("Shelter Roof Shape", shapes_list, index=shape_idx)

        st.markdown("#### Openings & Azimuth Orientation")
        cur_win = float(st.session_state.shelter_config.get("window_area", 1.8))
        cur_door = float(st.session_state.shelter_config.get("door_area", 2.0))
        cur_orient = int(st.session_state.shelter_config.get("orientation_deg", 0))

        st.session_state.shelter_config["window_area"] = st.number_input(
            "Window Glazing Area (m²)", min_value=0.0, max_value=10.0, value=min(max(0.0, cur_win), 10.0), step=0.2, format="%.1f"
        )
        st.session_state.shelter_config["door_area"] = st.number_input(
            "Door Openings Area (m²)", min_value=1.0, max_value=5.0, value=min(max(1.0, cur_door), 5.0), step=0.1, format="%.1f"
        )

        # Round orientation to step 5 to prevent step mismatches
        safe_orient = int(round(cur_orient / 5.0) * 5)
        st.session_state.shelter_config["orientation_deg"] = st.number_input(
            "Azimuth Orientation (° South = 0°)", min_value=-90, max_value=90, value=min(max(-90, safe_orient), 90), step=5
        )

    with col2:
        st.markdown("#### 🧊 Interactive 3D CAD Building Preview")
        fig_3d_cad = generate_shelter_3d_cad_figure(
            length=st.session_state.shelter_config["length"],
            width=st.session_state.shelter_config["width"],
            height=st.session_state.shelter_config["height"],
            shape=st.session_state.shelter_config["shape"],
            window_area=st.session_state.shelter_config["window_area"],
            door_area=st.session_state.shelter_config["door_area"],
            orientation_deg=st.session_state.shelter_config["orientation_deg"]
        )
        st.plotly_chart(fig_3d_cad, use_container_width=True)

    # Preview Area Metrics
    l = st.session_state.shelter_config["length"]
    w = st.session_state.shelter_config["width"]
    h = st.session_state.shelter_config["height"]
    gross_wall_area = 2 * (l + w) * h
    floor_area = l * w

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Floor Area", f"{floor_area:.1f} m²")
    m2.metric("Gross Wall Area", f"{gross_wall_area:.1f} m²")
    m3.metric("Window Ratio", f"{(st.session_state.shelter_config['window_area'] / gross_wall_area * 100):.1f}%")
    m4.metric("Building Volume", f"{(l * w * h):.1f} m³")

# ---------------------------------------------------------
# TAB 2: WALL CONSTRUCTION STACK
# ---------------------------------------------------------
with tab_wall:
    st.subheader("🧱 Wall Multi-Layer Composite Assembly")
    st.caption("Define inner structural masonry/timber layer and outer thermal insulation layers.")

    mat_options = mat_db.get_material_names()
    
    col_w1, col_w2 = st.columns([1, 1])

    with col_w1:
        st.markdown("#### Primary Wall Layer 1 (Structural)")
        w1_mat = st.selectbox("Layer 1 Material", mat_options, index=0, key="w1_mat")
        w1_thick = st.number_input("Layer 1 Thickness (m)", min_value=0.05, max_value=0.50, value=0.30, step=0.01, format="%.2f", key="w1_thick")

        st.markdown("#### Wall Layer 2 (Thermal Insulation)")
        w2_mat = st.selectbox("Layer 2 Material", mat_options, index=min(4, len(mat_options)-1), key="w2_mat")
        w2_thick = st.number_input("Layer 2 Thickness (m)", min_value=0.0, max_value=0.25, value=0.08, step=0.01, format="%.2f", key="w2_thick")

        w1_info = mat_db.get_material_by_name(w1_mat) or mat_db.get_material_by_id('mud_brick')
        w2_info = mat_db.get_material_by_name(w2_mat) or mat_db.get_material_by_id('xps_insulation')
        
        layers = [{"material_id": w1_info['id'], "thickness_m": w1_thick}]
        if w2_thick > 0:
            layers.append({"material_id": w2_info['id'], "thickness_m": w2_thick})

        st.session_state.wall_stack = mat_db.calculate_layer_stack(layers, "wall")

    with col_w2:
        st.markdown("#### 📊 Computed Wall Performance & Visual Layer Stack")
        ws = st.session_state.wall_stack
        
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color:#00F0FF; margin-top:0;">Wall U-Value: {ws['u_value']:.4f} W/m²K</h3>
            <p><b>Total Resistance (R):</b> {ws['r_total']:.3f} m²K/W</p>
            <p><b>Thermal Heat Capacity:</b> {ws['total_thermal_capacity']/1000:.1f} kJ/m²K</p>
            <p><b>Weight:</b> {ws['total_weight']:.1f} kg/m²</p>
        </div>
        """, unsafe_allow_html=True)

        df_layers = pd.DataFrame(ws['layers'])
        if not df_layers.empty:
            fig_stack = px.bar(
                df_layers,
                x='thickness_m',
                y='name',
                orientation='h',
                color='name',
                title="Layer Thickness Distribution (meters)",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_stack.update_layout(
                height=220,
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.6)",
                font=dict(color="#E2E8F0", family="Plus Jakarta Sans, sans-serif"),
                showlegend=False,
                margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig_stack, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: ROOF ASSEMBLY
# ---------------------------------------------------------
with tab_roof:
    st.subheader("🏠 Roof Insulation & Cladding Assembly")
    col_r1, col_r2 = st.columns([1, 1])

    with col_r1:
        st.markdown("#### Primary Roof Insulation Layer")
        r1_mat = st.selectbox("Roof Insulation Material", mat_options, index=min(6, len(mat_options)-1), key="r1_mat")
        r1_thick = st.number_input("Roof Insulation Thickness (m)", min_value=0.02, max_value=0.30, value=0.10, step=0.01, format="%.2f", key="r1_thick")

        st.markdown("#### Inner Structural Ceiling Layer")
        r2_mat = st.selectbox("Ceiling Lining Material", mat_options, index=min(8, len(mat_options)-1), key="r2_mat")
        r2_thick = st.number_input("Ceiling Lining Thickness (m)", min_value=0.01, max_value=0.10, value=0.04, step=0.005, format="%.3f", key="r2_thick")

        r1_info = mat_db.get_material_by_name(r1_mat) or mat_db.get_material_by_id('pu_foam')
        r2_info = mat_db.get_material_by_name(r2_mat) or mat_db.get_material_by_id('timber_wood')
        
        st.session_state.roof_stack = mat_db.calculate_layer_stack([
            {"material_id": r1_info['id'], "thickness_m": r1_thick},
            {"material_id": r2_info['id'], "thickness_m": r2_thick}
        ], "roof")

    with col_r2:
        rs = st.session_state.roof_stack
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color:#FF8F00; margin-top:0;">Roof U-Value: {rs['u_value']:.4f} W/m²K</h3>
            <p><b>Total Resistance (R):</b> {rs['r_total']:.3f} m²K/W</p>
            <p><b>Weight:</b> {rs['total_weight']:.1f} kg/m²</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: FLOOR ASSEMBLY
# ---------------------------------------------------------
with tab_floor:
    st.subheader("🦶 Ground Floor Slab & Insulation")
    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        st.markdown("#### Structural Base Slab")
        f1_mat = st.selectbox("Base Slab Material", mat_options, index=min(3, len(mat_options)-1), key="f1_mat")
        f1_thick = st.number_input("Base Slab Thickness (m)", min_value=0.05, max_value=0.30, value=0.15, step=0.01, format="%.2f", key="f1_thick")

        st.markdown("#### Under-Slab Thermal Insulation")
        f2_mat = st.selectbox("Under-Slab Insulation", mat_options, index=min(4, len(mat_options)-1), key="f2_mat")
        f2_thick = st.number_input("Under-Slab Insulation Thickness (m)", min_value=0.02, max_value=0.20, value=0.06, step=0.01, format="%.2f", key="f2_thick")

        f1_info = mat_db.get_material_by_name(f1_mat) or mat_db.get_material_by_id('concrete')
        f2_info = mat_db.get_material_by_name(f2_mat) or mat_db.get_material_by_id('xps_insulation')
        
        st.session_state.floor_stack = mat_db.calculate_layer_stack([
            {"material_id": f1_info['id'], "thickness_m": f1_thick},
            {"material_id": f2_info['id'], "thickness_m": f2_thick}
        ], "floor")

    with col_f2:
        fs = st.session_state.floor_stack
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color:#10B981; margin-top:0;">Floor U-Value: {fs['u_value']:.4f} W/m²K</h3>
            <p><b>Total Resistance (R):</b> {fs['r_total']:.3f} m²K/W</p>
            <p><b>Weight:</b> {fs['total_weight']:.1f} kg/m²</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 5: ADD CUSTOM MATERIAL
# ---------------------------------------------------------
with tab_custom:
    st.subheader("➕ Register Custom Building Material")
    with st.form("custom_mat_form"):
        c_name = st.text_input("Material Name", "Local Straw Clay Block")
        c_cat = st.selectbox("Category", ["Masonry", "Insulation", "Concrete", "Timber", "Bio-Based", "Composite"])
        col_cm1, col_cm2, col_cm3 = st.columns(3)
        with col_cm1:
            c_k = st.number_input("Thermal Conductivity k (W/m·K)", 0.001, 10.0, 0.12, 0.01)
        with col_cm2:
            c_rho = st.number_input("Density ρ (kg/m³)", 10.0, 5000.0, 600.0, 10.0)
        with col_cm3:
            c_cp = st.number_input("Specific Heat Capacity Cp (J/kg·K)", 100.0, 3000.0, 1200.0, 50.0)

        c_submit = st.form_submit_button("Add Material to Database")
        if c_submit:
            new_mat = mat_db.add_custom_material(c_name, c_cat, c_k, c_rho, c_cp)
            st.success(f"Successfully added custom material '{c_name}' (k={c_k} W/mK) to session material database!")

st.divider()

col_nav1, col_nav2 = st.columns([3, 1])
with col_nav2:
    if st.button("Next: Climate Conditions 🌤️", type="primary", use_container_width=True):
        st.switch_page("pages/3_🌤️_Climate_Conditions.py")
