import numpy as np
import pandas as pd

from .materials import MaterialDatabase
from .simulation import ThermalSimulationEngine

class ThermalOptimizer:
    """
    Multi-objective thermal design optimizer for high-altitude cold region shelters.
    Searches optimal combinations of insulation thickness, materials, orientation, and window ratio.
    """
    def __init__(self, mat_db=None):
        if mat_db is None:
            mat_db = MaterialDatabase()
        self.mat_db = mat_db
        self.sim_engine = ThermalSimulationEngine(self.mat_db)

    def optimize_design(self, base_shelter_config, weather_df, target_indoor_temp=18.0):
        """
        Runs parametric grid search over candidate material stacks, insulation thicknesses,
        orientation azimuths, and window sizes to find optimal thermal design configuration.
        """
        # Candidate materials to evaluate
        wall_materials = ['mud_brick', 'ceb', 'stone_masonry', 'timber_wood', 'concrete']
        insulation_materials = ['xps_insulation', 'pu_foam', 'mineral_wool', 'vip_panel', 'eps_insulation']
        
        insulation_thicknesses = [0.05, 0.08, 0.12, 0.15]
        window_areas = [1.0, 1.8, 2.5, 3.5] # m²
        orientations = [-30, 0, 30] # Azimuth degrees

        results_list = []

        # Floor and Roof fixed defaults for comparison search
        r_stack = self.mat_db.calculate_layer_stack([{"material_id": "pu_foam", "thickness_m": 0.10}], "roof")
        f_stack = self.mat_db.calculate_layer_stack([{"material_id": "xps_insulation", "thickness_m": 0.08}], "floor")

        # Iterate search space (smart grid sample)
        for w_mat in wall_materials[:3]: # Sample top structural materials
            for i_mat in insulation_materials[:3]: # Sample top insulations
                for t_ins in insulation_thicknesses:
                    for win_a in window_areas:
                        for orient in orientations:
                            w_stack = self.mat_db.calculate_layer_stack([
                                {"material_id": w_mat, "thickness_m": 0.25},
                                {"material_id": i_mat, "thickness_m": t_ins}
                            ], "wall")

                            cfg = dict(base_shelter_config)
                            cfg['window_area'] = win_a
                            cfg['orientation_deg'] = orient

                            sim_res = self.sim_engine.run_simulation(cfg, weather_df, w_stack, r_stack, f_stack)
                            kpis = sim_res['kpis']

                            w_mat_info = self.mat_db.get_material_by_id(w_mat)
                            i_mat_info = self.mat_db.get_material_by_id(i_mat)

                            # Multi-objective score calculation
                            # Penalty for dropping below target indoor temp
                            temp_penalty = max(0.0, target_indoor_temp - kpis['avg_indoor_temp']) * 15.0
                            # Heat loss penalty
                            loss_penalty = kpis['total_heat_loss_kwh'] * 2.0
                            # Solar gain reward
                            solar_reward = kpis['total_solar_gain_kwh'] * 3.0
                            # Cost penalty
                            est_cost = (w_mat_info['cost_index'] * 0.25 + i_mat_info['cost_index'] * t_ins) * 50

                            score = 100.0 - loss_penalty + solar_reward - temp_penalty - est_cost * 0.1

                            results_list.append({
                                "wall_material": w_mat_info['name'],
                                "insulation_material": i_mat_info['name'],
                                "insulation_thickness_cm": int(t_ins * 100),
                                "window_area_m2": win_a,
                                "orientation_deg": orient,
                                "wall_u_value": round(w_stack['u_value'], 3),
                                "avg_indoor_temp": round(kpis['avg_indoor_temp'], 2),
                                "min_indoor_temp": round(kpis['min_indoor_temp'], 2),
                                "total_heat_loss_kwh": round(kpis['total_heat_loss_kwh'], 2),
                                "total_solar_gain_kwh": round(kpis['total_solar_gain_kwh'], 2),
                                "thermal_efficiency_pct": round(kpis['thermal_efficiency_pct'], 1),
                                "optimization_score": round(score, 2)
                            })

        df_res = pd.DataFrame(results_list)
        df_sorted = df_res.sort_values(by="optimization_score", ascending=False).reset_index(drop=True)

        best_option = df_sorted.iloc[0].to_dict()

        return {
            "best_option": best_option,
            "top_10_designs": df_sorted.head(10),
            "all_search_results": df_sorted
        }

if __name__ == "__main__":
    from .weather import ClimateDataManager
    opt = ThermalOptimizer()
    w_df = ClimateDataManager().generate_synthetic_weather("Leh, Ladakh", 1)
    res = opt.optimize_design({"length": 6.0, "width": 4.0, "height": 2.4}, w_df)
    print("Best Option:", res['best_option'])
