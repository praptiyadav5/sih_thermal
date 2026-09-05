import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from backend.ui_theme import inject_custom_css, render_hero_banner

st.set_page_config(page_title="Climate Conditions | Thermal Shelter", page_icon="🌤️", layout="wide")
inject_custom_css()

weather_mgr = st.session_state.weather_mgr

render_hero_banner(
    title="🌤️ Global Climate Conditions & Environmental Boundary Hub",
    subtitle="Search ANY city or location worldwide, select cold region presets (Ladakh, Arctic, Alps, Rockies, Andes), or enter GPS coordinates.",
    badge_text="Weather Hub"
)

select_mode = st.radio(
    "Choose Location Input Method:",
    [
        "🔍 Search Any City / Location Worldwide",
        "🌎 Global Cold Region Presets (Ladakh, Arctic, Alps, Rockies, Andes)",
        "📍 Custom GPS Coordinates (Latitude / Longitude)",
        "⚙️ Manual Climate Override / Offline Mode"
    ],
    index=0,
    horizontal=True
)

st.divider()

col_c1, col_c2 = st.columns([1, 1])

with col_c1:
    st.subheader("📍 Location Selection")
    sim_days = st.slider("Simulation Duration (Days)", 1, 3, 1)

    if select_mode == "🔍 Search Any City / Location Worldwide":
        st.markdown("#### Search Any Place on Earth")
        search_query = st.text_input("Enter city, town, or region name (e.g., Reykjavik, Anchorage, Zermatt, Lhasa, Shimla):", "Reykjavik")
        
        if search_query:
            search_results = weather_mgr.search_world_locations(search_query)
            if search_results:
                search_options = {item['name']: item for item in search_results}
                selected_place_name = st.selectbox("Select matching location:", list(search_options.keys()))
                selected_item = search_options[selected_place_name]

                st.session_state.location_name = selected_item['name']
                st.session_state.selected_lat = selected_item['lat']
                st.session_state.selected_lon = selected_item['lon']
                st.session_state.selected_elev = selected_item['elevation_m']

                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color:#00F0FF; margin-top:0;">{selected_item['name']}</h4>
                    <p><b>Latitude:</b> {selected_item['lat']}° | <b>Longitude:</b> {selected_item['lon']}°</p>
                    <p><b>Elevation:</b> {selected_item['elevation_m']} m above sea level</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Fetch Live Weather for Selected Location", type="primary", use_container_width=True):
                    st.session_state.weather_df = weather_mgr.fetch_weather_data(
                        location_name=selected_item['name'],
                        lat=selected_item['lat'],
                        lon=selected_item['lon'],
                        simulation_days=sim_days
                    )
                    st.success(f"Successfully fetched live weather profile for {selected_item['name']}!")
            else:
                st.warning("No matching locations found. Try adjusting your search query.")

    elif select_mode == "🌎 Global Cold Region Presets (Ladakh, Arctic, Alps, Rockies, Andes)":
        preset_names = list(weather_mgr.locations.keys())
        loc_name = st.selectbox("Select Global Preset Location Profile:", preset_names, index=0)
        st.session_state.location_name = loc_name
        
        loc_details = weather_mgr.locations[loc_name]
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color:#FF8F00; margin-top:0;">{loc_name}</h4>
            <p><b>Region:</b> {loc_details.get('region', 'Global')}</p>
            <p><b>Coordinates:</b> {loc_details['lat']}°N, {loc_details['lon']}°E | <b>Elevation:</b> {loc_details['elevation_m']} m</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Fetch Weather Data for Preset Location", type="primary", use_container_width=True):
            st.session_state.weather_df = weather_mgr.fetch_weather_data(loc_name, simulation_days=sim_days)
            st.success(f"Successfully fetched weather profile for {loc_name}!")

    elif select_mode == "📍 Custom GPS Coordinates (Latitude / Longitude)":
        st.markdown("#### Enter Field Coordinates")
        c_lat = st.number_input("Latitude (°N / °S)", -90.0, 90.0, 34.1526, 0.0001)
        c_lon = st.number_input("Longitude (°E / °W)", -180.0, 180.0, 77.5771, 0.0001)
        c_elev = st.number_input("Elevation (meters)", 0, 8848, 3500, 50)
        
        custom_loc_name = f"Custom Site ({c_lat:.2f}°, {c_lon:.2f}°)"
        st.session_state.location_name = custom_loc_name

        if st.button("Fetch Weather for Custom Coordinates", type="primary", use_container_width=True):
            st.session_state.weather_df = weather_mgr.fetch_weather_data(
                location_name=custom_loc_name,
                lat=c_lat,
                lon=c_lon,
                simulation_days=sim_days
            )
            st.success(f"Fetched weather for custom site coordinates ({c_lat}°, {c_lon}°)")

with col_c2:
    st.subheader("⚙️ Environmental Overrides & Controls")
    if select_mode == "⚙️ Manual Climate Override / Offline Mode":
        m_temp = st.slider("Design Outdoor Ambient Temp (°C)", -45.0, 35.0, -15.0, 1.0)
        m_solar = st.slider("Peak Solar Irradiance (W/m²)", 0.0, 1300.0, 850.0, 50.0)
        m_wind = st.slider("Wind Speed (m/s)", 0.0, 30.0, 8.0, 0.5)

        if st.button("Apply Manual Custom Weather Curve", type="primary", use_container_width=True):
            st.session_state.weather_df = weather_mgr.generate_custom_manual_weather(m_temp, m_solar, m_wind, sim_days)
            st.success("Custom manual weather parameters generated successfully!")
    else:
        st.write("Click the button under your selected location option to query live Open-Meteo climate forecasts.")
        st.caption("Open-Meteo returns global hourly dry-bulb temperature, solar radiation, and wind speed forecasts anywhere on Earth.")

st.divider()

# Weather Preview Charts
st.subheader(f"📊 Hourly Environmental Boundary Profile — {st.session_state.get('location_name', 'Leh, Ladakh, India')}")

df_w = st.session_state.weather_df

fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    subplot_titles=(
        "🌡️ Outdoor Dry-Bulb Ambient Temperature (°C)",
        "☀️ Global Solar Irradiance (W/m²)",
        "💨 Wind Speed (m/s)"
    )
)

fig.add_trace(
    go.Scatter(x=df_w['time'], y=df_w['temperature_c'], mode='lines+markers', name='Temp (°C)', line=dict(color='#00F0FF', width=2.5)),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=df_w['time'], y=df_w['solar_radiation_w_m2'], mode='lines', fill='tozeroy', name='Solar (W/m²)', line=dict(color='#FF8F00', width=2)),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x=df_w['time'], y=df_w['wind_speed_m_s'], mode='lines', name='Wind Speed (m/s)', line=dict(color='#A855F7', width=2)),
    row=3, col=1
)

fig.update_layout(
    height=580,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15, 23, 42, 0.5)",
    margin=dict(l=20, r=20, t=35, b=20),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

col_nav1, col_nav2 = st.columns([3, 1])
with col_nav2:
    if st.button("Next: Launch Simulation ⚡", type="primary", use_container_width=True):
        st.switch_page("pages/4_⚡_Simulation.py")
