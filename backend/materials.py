import os
import pandas as pd
import numpy as np

# Standard air film thermal resistances (m²·K/W) according to ISO 6946 / ASHRAE
R_SI_WALL = 0.13    # Internal surface resistance for walls
R_SE_WALL = 0.04    # External surface resistance for walls (exposed to wind)
R_SI_ROOF = 0.10    # Internal surface resistance for heat flow up/down
R_SE_ROOF = 0.04    # External surface resistance for roof
R_SI_FLOOR = 0.17   # Internal surface resistance for floor
R_SE_FLOOR = 0.17   # Ground contact / underfloor resistance

class MaterialDatabase:
    """
    Database and calculator for construction thermal materials, U-values,
    layer stacks, and heat capacity properties for cold-region shelter analysis.
    """
    def __init__(self, csv_path=None):
        if csv_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_path = os.path.join(base_dir, "data", "materials.csv")
        self.csv_path = csv_path
        self.df = self._load_data()

    def _load_data(self):
        if os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            return df
        else:
            # Fallback default dataset
            data = [
                {"id": "mud_brick", "name": "Traditional Mud Brick (Sun-Dried)", "category": "Masonry", "conductivity_k": 0.75, "density_rho": 1800, "specific_heat_cp": 880, "emissivity": 0.90, "solar_absorptivity": 0.70, "cost_index": 1.0, "description": "High thermal mass traditional material used in Ladakh"},
                {"id": "ceb", "name": "Compressed Earth Block (CEB)", "category": "Masonry", "conductivity_k": 0.95, "density_rho": 1950, "specific_heat_cp": 920, "emissivity": 0.88, "solar_absorptivity": 0.65, "cost_index": 1.5, "description": "Stabilized earth block offering good thermal mass"},
                {"id": "stone_masonry", "name": "Granite / Slate Stone Masonry", "category": "Masonry", "conductivity_k": 2.20, "density_rho": 2600, "specific_heat_cp": 840, "emissivity": 0.92, "solar_absorptivity": 0.75, "cost_index": 2.0, "description": "Local stone material"},
                {"id": "concrete", "name": "Reinforced Concrete", "category": "Concrete", "conductivity_k": 1.50, "density_rho": 2300, "specific_heat_cp": 900, "emissivity": 0.90, "solar_absorptivity": 0.60, "cost_index": 2.5, "description": "Standard structural concrete"},
                {"id": "xps_insulation", "name": "Extruded Polystyrene (XPS)", "category": "Insulation", "conductivity_k": 0.032, "density_rho": 35, "specific_heat_cp": 1450, "emissivity": 0.90, "solar_absorptivity": 0.30, "cost_index": 3.5, "description": "Moisture-resistant thermal insulation board"},
                {"id": "eps_insulation", "name": "Expanded Polystyrene (EPS)", "category": "Insulation", "conductivity_k": 0.038, "density_rho": 25, "specific_heat_cp": 1300, "emissivity": 0.90, "solar_absorptivity": 0.30, "cost_index": 2.5, "description": "Cost-effective cellular insulation"},
                {"id": "pu_foam", "name": "Polyurethane (PU) Foam Board", "category": "Insulation", "conductivity_k": 0.024, "density_rho": 32, "specific_heat_cp": 1400, "emissivity": 0.90, "solar_absorptivity": 0.30, "cost_index": 4.2, "description": "Rigid foam insulation with very low conductivity"},
                {"id": "mineral_wool", "name": "Rock Mineral Wool", "category": "Insulation", "conductivity_k": 0.035, "density_rho": 80, "specific_heat_cp": 840, "emissivity": 0.90, "solar_absorptivity": 0.30, "cost_index": 3.0, "description": "Fire-resistant mineral wool insulation"},
                {"id": "timber_wood", "name": "Deodar Cedar / Spruce Wood", "category": "Timber", "conductivity_k": 0.13, "density_rho": 520, "specific_heat_cp": 1600, "emissivity": 0.85, "solar_absorptivity": 0.50, "cost_index": 3.8, "description": "Natural timber providing insulation & structure"},
                {"id": "vip_panel", "name": "Vacuum Insulated Panel (VIP)", "category": "Insulation", "conductivity_k": 0.007, "density_rho": 200, "specific_heat_cp": 800, "emissivity": 0.90, "solar_absorptivity": 0.20, "cost_index": 9.0, "description": "Ultra-thin super insulation panel"}
            ]
            return pd.DataFrame(data)

    def get_all_materials(self):
        return self.df.to_dict('records')

    def get_material_names(self):
        return self.df['name'].tolist()

    def get_material_by_id(self, mat_id):
        match = self.df[self.df['id'] == mat_id]
        if not match.empty:
            return match.iloc[0].to_dict()
        return None

    def get_material_by_name(self, name):
        match = self.df[self.df['name'] == name]
        if not match.empty:
            return match.iloc[0].to_dict()
        return None

    def add_custom_material(self, name, category, k, rho, cp, emissivity=0.9, solar_absorptivity=0.6, cost_index=3.0, description="Custom user-defined material"):
        mat_id = "custom_" + name.lower().replace(" ", "_")
        new_row = {
            "id": mat_id,
            "name": name,
            "category": category,
            "conductivity_k": float(k),
            "density_rho": float(rho),
            "specific_heat_cp": float(cp),
            "emissivity": float(emissivity),
            "solar_absorptivity": float(solar_absorptivity),
            "cost_index": float(cost_index),
            "description": description
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        # Optionally save to CSV
        try:
            self.df.to_csv(self.csv_path, index=False)
        except Exception:
            pass
        return new_row

    def calculate_layer_stack(self, layers, component_type="wall", extra_wind_speed=0.0):
        """
        Calculates composite thermal performance for a stack of material layers.
        layers format: [{'material_id': 'xps_insulation', 'thickness_m': 0.08}, ...]
        Returns dict containing U_value (W/m²K), Total R (m²K/W), Thermal Mass (J/m²K), Weight (kg/m²)
        """
        r_si = R_SI_WALL if component_type == "wall" else (R_SI_ROOF if component_type == "roof" else R_SI_FLOOR)
        
        # Adjust external convection resistance based on wind speed if specified: h_se = 5.7 + 3.8 * v
        if extra_wind_speed > 0:
            h_se = 5.7 + 3.8 * extra_wind_speed
            r_se = 1.0 / h_se
        else:
            r_se = R_SE_WALL if component_type == "wall" else (R_SE_ROOF if component_type == "roof" else R_SE_FLOOR)

        r_layers = 0.0
        total_thermal_capacity = 0.0 # J/(m²·K)
        total_weight = 0.0 # kg/m²
        evaluated_layers = []

        for layer in layers:
            mat_id = layer.get('material_id')
            mat = self.get_material_by_id(mat_id)
            if not mat:
                mat = self.get_material_by_name(layer.get('material_name', ''))
            
            if not mat:
                # Default fallback if unknown material
                mat = self.get_material_by_id('concrete')

            t = float(layer.get('thickness_m', 0.1))
            k = float(mat['conductivity_k'])
            rho = float(mat['density_rho'])
            cp = float(mat['specific_heat_cp'])

            r_layer = t / k if k > 0 else 0.01
            r_layers += r_layer

            cap = rho * cp * t
            weight = rho * t

            total_thermal_capacity += cap
            total_weight += weight

            evaluated_layers.append({
                "name": mat['name'],
                "thickness_m": t,
                "conductivity_k": k,
                "r_value": r_layer,
                "density_rho": rho,
                "heat_capacity_j_m2k": cap,
                "weight_kg_m2": weight
            })

        r_total = r_si + r_layers + r_se
        u_value = 1.0 / r_total if r_total > 0 else 10.0

        return {
            "component_type": component_type,
            "u_value": u_value, # W/m²K
            "r_total": r_total, # m²K/W
            "r_layers": r_layers,
            "r_si": r_si,
            "r_se": r_se,
            "total_thermal_capacity": total_thermal_capacity, # J/m²K
            "total_weight": total_weight, # kg/m²
            "layers": evaluated_layers
        }

if __name__ == "__main__":
    db = MaterialDatabase()
    print("Loaded materials:", len(db.get_all_materials()))
    stack = db.calculate_layer_stack([
        {"material_id": "stone_masonry", "thickness_m": 0.25},
        {"material_id": "xps_insulation", "thickness_m": 0.10}
    ], component_type="wall", extra_wind_speed=8.0)
    print("Wall U-Value:", stack['u_value'], "W/m²K")
