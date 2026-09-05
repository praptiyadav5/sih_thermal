"""
PyAnsys / PyMechanical Parametric Geometry Generator
Generates ANSYS APDL geometry creation scripts for thermal shelters.
"""

def generate_ansys_geometry_apdl(length, width, height, shape="Rectangular", roof_height=0.8, window_area=1.5, door_area=2.0, orientation_deg=0.0):
    """
    Generates APDL solid model generation block for thermal shelter FEA.
    """
    apdl = f"""! =========================================================
! ANSYS Thermal Shelter Solid Parametric Geometry
! Length: {length}m | Width: {width}m | Wall Height: {height}m | Shape: {shape}
! Window Area: {window_area}m2 | Door Area: {door_area}m2 | Orientation: {orientation_deg}°
! =========================================================
/PREP7
ET, 1, SOLID70              ! 3D 8-Node Thermal Solid Element
ET, 2, SHELL57              ! 3D Thermal Shell for Thin Surfaces

! Define Dimension Parameters
L_SHELTER = {length:.3f}
W_SHELTER = {width:.3f}
H_EAVE    = {height:.3f}
H_RIDGE   = {height + (roof_height if shape in ['Gable', 'Monoslope'] else 0.0):.3f}
AZIMUTH   = {orientation_deg:.1f}

! Build Main Bounding Solid (Volume 1)
BLOCK, 0, L_SHELTER, 0, W_SHELTER, 0, H_EAVE

! Create Opening Cutout Selectors
WIN_AREA = {window_area:.2f}
DOOR_AREA = {door_area:.2f}

! Set Element Attributes & Mesh Parameters
ESIZE, 0.25                  ! Global Mesh Element Size (250mm)
VMESH, ALL                   ! Mesh Solid Volume

! Rotate Local Coordinate System for Azimuth Alignment
LOCAL, 11, 0, L_SHELTER/2, W_SHELTER/2, 0, AZIMUTH, 0, 0
CSYS, 11
"""
    return apdl
