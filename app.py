import os
import sys
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.session_state import ensure_session_state

st.set_page_config(
    page_title="Thermal Shelter Studio",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize shared application state
ensure_session_state()

# Streamlit Multi-Page Navigation Router
# Defines clean sidebar page list and removes 'app' entry from sidebar
pg = st.navigation(
    [
        st.Page("pages/1_🏠_Home.py", title="Home", icon="🏠", default=True),
        st.Page("pages/2_📐_Shelter_Design.py", title="Shelter Design", icon="📐"),
        st.Page("pages/3_🌤️_Climate_Conditions.py", title="Climate Conditions", icon="🌤️"),
        st.Page("pages/4_⚡_Simulation.py", title="Simulation", icon="⚡"),
        st.Page("pages/5_📊_Results.py", title="Results", icon="📊"),
        st.Page("pages/6_⚖️_Comparison.py", title="Comparison", icon="⚖️"),
        st.Page("pages/7_🚀_Optimization.py", title="Optimization", icon="🚀"),
    ],
    position="sidebar"
)

pg.run()

