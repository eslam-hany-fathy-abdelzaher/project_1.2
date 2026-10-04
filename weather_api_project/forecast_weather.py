import sqlite3
import requests
from datetime import datetime

def update_and_fetch_forecast():
    latitude = 40.7128
    longitude = -74.0060
    city_name = "New York"
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_direction_10m_dominant&timezone=auto"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            
            times = daily.get("time", [])
            temps_max = daily.get("temperature_2m_max", [])
            temps_min = daily.get("temperature_2m_min", [])
            winds = daily.get("wind_speed_10m_max", [])
            wind_dirs = daily.get("wind_direction_10m_dominant", [])
            
            conn = sqlite3.connect("weather_data.db")
            cursor = conn.cursor()
            
            for i in range(len(times)):
                date_str = times[i]
                t_max = temps_max[i]
                t_min = temps_min[i]
                temperature = (t_max + t_min) / 2 if t_max is not None and t_min is not None else 0.0
                wind_speed = winds[i] if winds[i] is not None else 0.0
                wind_direction = wind_dirs[i] if wind_dirs[i] is not None else 0.0
                
                today_str = datetime.now().strftime("%Y-%m-%d")
                data_type = 'A' if date_str <= today_str else 'P'
                
                cursor.execute("""
                    INSERT OR REPLACE INTO weather (date, city, temperature, wind_speed, wind_direction, data_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (date_str, city_name, temperature, wind_speed, wind_direction, data_type))
                
            conn.commit()
            conn.close()
            print("✅ Forecast data fetched and updated successfully!")
        else:
            print("Failed to fetch forecast, status code:", response.status_code)
    except Exception as e:
        print("An error occurred while fetching forecast:", e)

if __name__ == "__main__":
    update_and_fetch_forecast()