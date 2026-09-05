# 🏔️ Thermal Shelter Simulation & Optimization Platform (Ladakh Region)

A complete production-ready web application for designing, simulating, and optimizing high-altitude thermal shelters tailored for severe cold regions like Ladakh, India (Leh, Kargil, Dras, Nyoma, Pangong).

The application features:
- **Streamlit & Plotly Dashboard UI**: 7 dedicated pages for building CAD layout, envelope construction layer stacks, climate conditions, solver setup, interactive thermal heatmaps, multi-design benchmarking, and multi-objective optimization.
- **Dual-Mode Thermal Solver Architecture**:
  - **PyAnsys / PyMechanical Live Integration**: Auto-generates PyMechanical APDL scripts, sets up 3D thermal solid elements (`SOLID70`), transfers environmental convection & solar flux boundary conditions, and extracts nodal thermal results.
  - **High-Fidelity Physics Numerical Fallback Solver**: Multi-layer transient energy balance solver for operation when ANSYS is not installed on the local system.
- **Open-Meteo Weather API**: Fetches hourly temperature, global horizontal solar irradiance, and wind speed for Ladakh region coordinates, with offline synthetic climate profile fallbacks.
- **Cold-Region Building Materials Database**: Presets for traditional mud brick (Trombe wall), compressed earth blocks (CEB), granite stone masonry, XPS/EPS/PU foam insulation, vacuum insulated panels (VIP), timber wood, and multi-glazed windows.
- **Automated Multi-Objective Optimizer**: Searches material choices, insulation thicknesses, azimuth orientations, and window ratios to minimize heat loss and maximize solar heat gain.

---

## 📁 Repository Directory Structure

```text
thermal_shelter/
├── app.py                      # Main Streamlit application entrypoint & session state orchestrator
├── requirements.txt            # Python package dependencies
├── README.md                   # Setup documentation & PyAnsys configuration guide
├── pages/
│   ├── 1_🏠_Home.py           # Project introduction, Ladakh climate challenge, workflow overview
│   ├── 2_📐_Shelter_Design.py  # Parametric geometry, orientation, window/door ratios, and layer stack editor
│   ├── 3_🌤️_Climate_Conditions.py # Open-Meteo weather API client & manual environmental parameter overrides
│   ├── 4_⚡_Simulation.py      # Pre-simulation parameter audit, ANSYS engine monitor, and solver launcher
│   ├── 5_📊_Results.py        # Thermal dashboard with KPIs, Plotly heat loss curves, and 3D spatial surface heatmaps
│   ├── 6_⚖️_Comparison.py     # Multi-design comparative benchmarking (up to 4 shelter designs side-by-side)
│   └── 7_🚀_Optimization.py   # Multi-objective thermal design optimizer (grid search & heuristic ranking)
├── backend/
│   ├── __init__.py
│   ├── weather.py              # Open-Meteo weather API wrapper with Ladakh location presets & offline fallback
│   ├── materials.py            # Material database loader, layer stack U-value & R-value calculator
│   ├── simulation.py           # Dual-mode thermal solver engine (PyAnsys bridge + transient physics FEA)
│   └── optimizer.py            # Parametric multi-objective thermal design optimizer
├── ansys/
│   ├── __init__.py
│   ├── mechanical_script.py    # PyMechanical script builder & solver availability checker
│   ├── geometry.py             # ANSYS APDL solid geometry command generator
│   ├── materials.py            # ANSYS APDL material property definition exporter (`MP, KXX`, `MP, DENS`, `MP, C`)
│   ├── boundary_conditions.py  # Convective heat transfer coefficient $h(v)$, solar flux, ambient boundary mapper
│   └── results.py              # ANSYS `.rst` and output summary result parser
└── data/
    └── materials.csv           # Database of cold-climate thermal materials & properties
```

---

## ⚙️ Installation & Running Locally

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Install Dependencies
Navigate to the project folder and install required dependencies:
```bash
cd thermal_shelter
pip install -r requirements.txt
```

### 3. Launch Streamlit Application
Run the Streamlit server:
```bash
streamlit run app.py
```
The application will open automatically in your web browser at `http://localhost:8501`.

---

## 🔧 ANSYS Mechanical & PyAnsys Setup Guide

To run live FEA thermal simulations directly inside ANSYS Mechanical:

1. **Install ANSYS Mechanical / MAPDL**: Ensure ANSYS Student or Enterprise (2022 R1 or newer) is installed on your Windows host machine.
2. **Install PyAnsys Python Core Libraries**:
   ```bash
   pip install ansys-mapdl-core ansys-mechanical-core ansys-dpf-core
   ```
3. **Verify License & Path**: Ensure `ANSYS_CMD` or `ANSYSLMD_LICENSE_FILE` environment variables point to your local ANSYS installation path (e.g. `C:\Program Files\ANSYS Inc\v232\ansys\bin\winx64\ansys232.exe`).
4. When PyAnsys is detected, the application automatically toggles the solver badge to **🟢 LIVE ANSYS MECHANICAL** and executes APDL thermal solvers via PyMechanical.

---

## 📄 Application Pages Overview

1. **Home (`pages/1_🏠_Home.py`)**: Explains the extreme high-altitude winter climate of Ladakh, physical principles of passive solar heating (Trombe walls, U-values, envelope mass), and system workflow.
2. **Shelter Design (`pages/2_📐_Shelter_Design.py`)**: Parametric geometry sliders (Length, Width, Height, Roof shape, Azimuth orientation), glazing/door areas, and multi-layer wall, roof, and floor construction assembly editor.
3. **Climate Conditions (`pages/3_🌤️_Climate_Conditions.py`)**: Preset high-altitude locations (Leh, Dras, Kargil, Nyoma, Pangong Lake, Padum, Nubra Valley), Open-Meteo weather API integration, manual parameter overrides, and hourly time-series preview charts.
4. **Simulation (`pages/4_⚡_Simulation.py`)**: Parameter audit, solver status indicator (PyMechanical vs Fallback physics), auto-generated APDL code inspector, and simulation execution control panel.
5. **Results (`pages/5_📊_Results.py`)**: Performance metrics (Peak/Avg Indoor Temp, Daily Heat Loss, Solar Heat Gain, Thermal Efficiency Index), Plotly temperature curves, component heat loss breakdown, and 3D spatial indoor thermal distribution surface heatmap.
6. **Comparison (`pages/6_⚖️_Comparison.py`)**: Benchmarking up to 4 shelter design profiles side-by-side under identical Ladakh weather conditions with comparative charts and ranking tables.
7. **Optimization (`pages/7_🚀_Optimization.py`)**: Multi-objective parameter optimizer searching wall materials, insulation thicknesses, orientation azimuths, and window sizes to minimize heat loss and maximize solar gain.
