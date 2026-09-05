import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Worldwide Preset Locations (Categorized by Extreme Climate Regions)
GLOBAL_PRESET_LOCATIONS = {
    # High Altitude Himalaya & Ladakh
    "Leh, Ladakh, India": {"lat": 34.1526, "lon": 77.5771, "elevation_m": 3524, "region": "Himalayas / Ladakh"},
    "Dras, Kargil, India (Coldest Inhabited Place in India)": {"lat": 34.4290, "lon": 75.7662, "elevation_m": 3280, "region": "Himalayas / Ladakh"},
    "Kargil Town, India": {"lat": 34.5539, "lon": 76.1311, "elevation_m": 2676, "region": "Himalayas / Ladakh"},
    "Nyoma (Changthang Plateau), India": {"lat": 33.2036, "lon": 78.6475, "elevation_m": 4180, "region": "Himalayas / Ladakh"},
    "Pangong Lake Shore (Spangmik), India": {"lat": 33.9100, "lon": 78.4600, "elevation_m": 4250, "region": "Himalayas / Ladakh"},
    "Lhasa, Tibet": {"lat": 29.6524, "lon": 91.1721, "elevation_m": 3656, "region": "Tibetan Plateau"},
    "Shimla, Himachal Pradesh, India": {"lat": 31.1048, "lon": 77.1734, "elevation_m": 2276, "region": "Himalayas"},

    # Arctic & Sub-Arctic Regions
    "Anchorage, Alaska, USA": {"lat": 61.2181, "lon": -149.9003, "elevation_m": 31, "region": "Arctic & Sub-Arctic"},
    "Fairbanks, Alaska, USA": {"lat": 64.8401, "lon": -147.7200, "elevation_m": 136, "region": "Arctic & Sub-Arctic"},
    "Tromsø, Norway": {"lat": 69.6492, "lon": 18.9553, "elevation_m": 20, "region": "Arctic & Sub-Arctic"},
    "Reykjavik, Iceland": {"lat": 64.1466, "lon": -21.9426, "elevation_m": 15, "region": "Nordic / Arctic"},
    "Nuuk, Greenland": {"lat": 64.1814, "lon": -51.7214, "elevation_m": 5, "region": "Arctic"},
    "Yellowknife, Northwest Territories, Canada": {"lat": 62.4540, "lon": -114.3718, "elevation_m": 206, "region": "Sub-Arctic"},

    # Alpine & Mountainous Regions
    "Zermatt, Switzerland (Alps)": {"lat": 46.0207, "lon": 7.7491, "elevation_m": 1620, "region": "European Alps"},
    "Chamonix, Mont-Blanc, France": {"lat": 45.9237, "lon": 6.8694, "elevation_m": 1035, "region": "European Alps"},
    "Innsbruck, Austria": {"lat": 47.2692, "lon": 11.4041, "elevation_m": 574, "region": "European Alps"},
    "Aspen, Colorado, USA (Rocky Mountains)": {"lat": 39.1911, "lon": -106.8175, "elevation_m": 2405, "region": "Rocky Mountains"},
    "Banff, Alberta, Canada": {"lat": 51.1784, "lon": -115.5708, "elevation_m": 1383, "region": "Canadian Rockies"},
    "La Paz, Bolivia (Andes Plateau)": {"lat": -16.4897, "lon": -68.1193, "elevation_m": 3640, "region": "South American Andes"},

    # Asia Cold Regions
    "Ulaanbaatar, Mongolia (Coldest World Capital)": {"lat": 47.9212, "lon": 106.9186, "elevation_m": 1350, "region": "Central Asia"},
    "Sapporo, Hokkaido, Japan": {"lat": 43.0618, "lon": 141.3545, "elevation_m": 29, "region": "East Asia"},
    "Harbin, Heilongjiang, China": {"lat": 45.8038, "lon": 126.5349, "elevation_m": 150, "region": "East Asia"}
}

class ClimateDataManager:
    """
    Retrieves weather data from Open-Meteo API for any location worldwide
    or generates realistic high-altitude synthetic climate datasets.
    Includes Open-Meteo World Geocoding Search integration.
    """
    def __init__(self):
        self.locations = GLOBAL_PRESET_LOCATIONS

    def search_world_locations(self, query):
        """
        Searches any city, region, or location worldwide using Open-Meteo Geocoding API.
        Returns a list of matching location dicts with name, country, latitude, longitude, and elevation.
        """
        if not query or len(query.strip()) < 2:
            return []

        try:
            url = f"https://geocoding-api.open-meteo.com/v1/search?name={requests.utils.quote(query)}&count=10&language=en&format=json"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                formatted = []
                for item in results:
                    city_name = item.get("name", "")
                    country = item.get("country", "")
                    admin1 = item.get("admin1", "")
                    lat = item.get("latitude")
                    lon = item.get("longitude")
                    elevation = item.get("elevation", 0)

                    display_label = f"{city_name}"
                    if admin1:
                        display_label += f", {admin1}"
                    if country:
                        display_label += f", {country}"

                    formatted.append({
                        "name": display_label,
                        "city": city_name,
                        "country": country,
                        "lat": lat,
                        "lon": lon,
                        "elevation_m": elevation
                    })
                return formatted
        except Exception as e:
            print(f"Geocoding API search error: {e}")
        return []

    def fetch_weather_data(self, location_name="Leh, Ladakh, India", lat=None, lon=None,
                           start_date=None, simulation_days=1, use_offline_fallback=False):
        """
        Fetches hourly weather data (Temperature °C, Solar Irradiance W/m², Wind Speed m/s)
        for any location on Earth specified by lat/lon or location_name.
        """
        if lat is None or lon is None:
            loc = self.locations.get(location_name, self.locations["Leh, Ladakh, India"])
            lat = loc["lat"]
            lon = loc["lon"]

        if use_offline_fallback:
            return self.generate_synthetic_weather(location_name, simulation_days)

        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&hourly=temperature_2m,direct_normal_irradiance,diffuse_radiation,wind_speed_10m,relative_humidity_2m"
                f"&forecast_days={max(1, min(simulation_days, 7))}"
                f"&timezone=auto"
            )
            response = requests.get(url, timeout=6)
            if response.status_code == 200:
                data = response.json()
                hourly = data.get("hourly", {})
                times = hourly.get("time", [])
                temps = hourly.get("temperature_2m", [])
                direct_irr = hourly.get("direct_normal_irradiance", [])
                diffuse_irr = hourly.get("diffuse_radiation", [])
                wind = hourly.get("wind_speed_10m", [])

                solar_ghi = np.array(direct_irr, dtype=float) * 0.7 + np.array(diffuse_irr, dtype=float)
                solar_ghi = np.clip(solar_ghi, 0, 1300)

                df = pd.DataFrame({
                    "hour": list(range(len(times))),
                    "time": times,
                    "temperature_c": temps,
                    "solar_radiation_w_m2": solar_ghi,
                    "wind_speed_m_s": wind
                })
                return df
            else:
                print(f"Open-Meteo API returned status {response.status_code}. Using synthetic fallback weather.")
                return self.generate_synthetic_weather(location_name, simulation_days)
        except Exception as e:
            print(f"Weather API fetch failed ({str(e)}). Falling back to synthetic climate model.")
            return self.generate_synthetic_weather(location_name, simulation_days)

    def generate_synthetic_weather(self, location_name="Leh, Ladakh, India", simulation_days=1, season="Winter"):
        """
        Generates realistic hourly diurnal weather curves.
        """
        total_hours = simulation_days * 24
        hours = np.arange(total_hours)

        if "Dras" in location_name or "Fairbanks" in location_name or "Yellowknife" in location_name:
            t_min, t_max, solar_peak, wind_base = -24.0, -10.0, 800.0, 8.0
        elif "Pangong" in location_name or "Nyoma" in location_name or "Ulaanbaatar" in location_name:
            t_min, t_max, solar_peak, wind_base = -18.0, -5.0, 950.0, 10.0
        elif "Zermatt" in location_name or "Banff" in location_name or "Aspen" in location_name:
            t_min, t_max, solar_peak, wind_base = -12.0, -2.0, 750.0, 5.0
        else: # Default Leh / High Altitude Cold
            t_min, t_max, solar_peak, wind_base = -15.0, -2.0, 900.0, 6.0

        temp_curve = t_min + (t_max - t_min) * 0.5 * (1 + np.sin(2 * np.pi * (hours - 8) / 24))
        temp_curve += np.random.normal(0, 0.4, total_hours)

        solar_curve = np.zeros(total_hours)
        for h in range(total_hours):
            hour_of_day = h % 24
            if 7 <= hour_of_day <= 17:
                solar_curve[h] = solar_peak * np.sin(np.pi * (hour_of_day - 7) / 10) ** 1.5

        wind_curve = np.clip(wind_base + 3.0 * np.sin(2 * np.pi * (hours - 12) / 24) + np.random.normal(0, 1.0, total_hours), 1.0, 25.0)

        times = [(datetime.now().replace(minute=0, second=0) + timedelta(hours=int(h))).strftime("%Y-%m-%d %H:00") for h in range(total_hours)]

        return pd.DataFrame({
            "hour": hours,
            "time": times,
            "temperature_c": np.round(temp_curve, 2),
            "solar_radiation_w_m2": np.round(solar_curve, 1),
            "wind_speed_m_s": np.round(wind_curve, 1)
        })

    def generate_custom_manual_weather(self, constant_temp=-12.0, constant_solar=650.0, constant_wind=6.0, simulation_days=1):
        """
        Creates weather dataframe from manual constant/diurnal user inputs.
        """
        total_hours = simulation_days * 24
        hours = np.arange(total_hours)

        temp_curve = constant_temp + 5.0 * np.sin(2 * np.pi * (hours - 8) / 24)
        solar_curve = np.zeros(total_hours)
        for h in range(total_hours):
            hour_of_day = h % 24
            if 7 <= hour_of_day <= 17:
                solar_curve[h] = constant_solar * np.sin(np.pi * (hour_of_day - 7) / 10)

        wind_curve = np.full(total_hours, constant_wind)
        times = [(datetime.now().replace(minute=0, second=0) + timedelta(hours=int(h))).strftime("%Y-%m-%d %H:00") for h in range(total_hours)]

        return pd.DataFrame({
            "hour": hours,
            "time": times,
            "temperature_c": np.round(temp_curve, 2),
            "solar_radiation_w_m2": np.round(solar_curve, 1),
            "wind_speed_m_s": np.round(wind_curve, 1)
        })

if __name__ == "__main__":
    weather_mgr = ClimateDataManager()
    res = weather_mgr.search_world_locations("Reykjavik")
    print("Found world locations:", res)
