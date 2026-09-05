"""
PyAnsys / PyMechanical Thermal Boundary Condition Generator
Applies environmental loads (convection, radiation, solar flux, ground temp) in APDL.
"""

def generate_ansys_boundary_conditions_apdl(ambient_temp, solar_flux, wind_speed, ground_temp=2.0):
    """
    Generates APDL boundary condition commands.
    """
    # Convective film coefficient (W/m²·K) according to McAdams / ISO relation: h = 5.7 + 3.8 * v
    h_conv = 5.7 + 3.8 * float(wind_speed)

    apdl = f"""! =========================================================
! ANSYS Thermal Environmental Boundary Conditions
! T_ambient: {ambient_temp:.2f}°C | Solar Flux: {solar_flux:.1f} W/m2 | Wind: {wind_speed:.1f} m/s (h={h_conv:.2f})
! =========================================================

! Define Convection Boundary on External Wall & Roof Surfaces
NSEL, S, LOC, Z, H_EAVE, H_RIDGE    ! Select roof nodes
NSEL, A, LOC, X, 0                  ! Select West wall nodes
NSEL, A, LOC, X, L_SHELTER          ! Select East wall nodes
NSEL, A, LOC, Y, 0                  ! Select South wall nodes
NSEL, A, LOC, Y, W_SHELTER          ! Select North wall nodes

SF, ALL, CONV, {h_conv:.2f}, {ambient_temp:.2f}

! Apply Solar Irradiance Heat Flux to Exposed South & Roof Surfaces
NSEL, S, LOC, Y, 0                  ! South face
NSEL, A, LOC, Z, H_EAVE             ! Roof face
SF, ALL, HFLUX, {solar_flux * 0.85:.2f}

! Ground Contact Boundary Condition on Floor (Z = 0)
NSEL, S, LOC, Z, 0                  ! Floor nodes
SF, ALL, CONV, 3.5, {ground_temp:.2f}  ! Ground thermal resistance ~0.28 m2K/W, T_ground={ground_temp}°C

ALLSEL, ALL
"""
    return apdl
