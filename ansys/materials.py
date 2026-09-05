"""
PyAnsys / PyMechanical Material Command Generator
Converts material properties into ANSYS Mechanical APDL commands.
"""

def generate_ansys_material_apdl(mat_id_num, name, k, rho, cp, emissivity=0.9, solar_absorptivity=0.6):
    """
    Generates APDL (ANSYS Parametric Design Language) material definition block.
    """
    apdl = f"""! =========================================================
! ANSYS Thermal Material Definition: {name} (Mat ID: {mat_id_num})
! =========================================================
MP, KXX,  {mat_id_num}, {k:.4f}     ! Thermal Conductivity (W/m-K)
MP, DENS, {mat_id_num}, {rho:.1f}    ! Density (kg/m3)
MP, C,    {mat_id_num}, {cp:.1f}     ! Specific Heat (J/kg-K)
MP, EMIS, {mat_id_num}, {emissivity:.2f} ! Surface Emissivity
! Custom APDL solar absorptivity parameter
PARSAV, ALL
ABSORP_{mat_id_num} = {solar_absorptivity:.2f}
"""
    return apdl

def generate_composite_ansys_materials(layer_stack, start_mat_id=1):
    """
    Generates APDL block for a multi-layer composite stack.
    """
    apdl_blocks = []
    current_id = start_mat_id
    for layer in layer_stack['layers']:
        apdl = generate_ansys_material_apdl(
            mat_id_num=current_id,
            name=layer['name'],
            k=layer['conductivity_k'],
            rho=layer['density_rho'],
            cp=layer['heat_capacity_j_m2k'] / (layer['density_rho'] * layer['thickness_m']) if layer['density_rho'] > 0 and layer['thickness_m'] > 0 else 900
        )
        apdl_blocks.append(apdl)
        current_id += 1
    return "\n".join(apdl_blocks)
