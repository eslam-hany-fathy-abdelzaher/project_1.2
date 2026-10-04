import sqlite3
import requests
from datetime import datetime, timedelta

def fetch_and_store_historical_data():
    latitude = 40.7128
    longitude = -74.0060
    city_name = "New York"
    
    # نحدد الفترة مثلاً آخر سنة أو سنتين لتوفير الوقت وسرعة التنفيذ، أو من 2023 مثلاً
    start_date = "2023-01-01"
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max"
    
    print("⏳ Fetching all historical data in one fast request...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            
            times = daily.get("time", [])
            temps_max = daily.get("temperature_2m_max", [])
            temps_min = daily.get("temperature_2m_min", [])
            winds = daily.get("wind_speed_10m_max", [])
            
            conn = sqlite3.connect("weather_data.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather (
                    date TEXT PRIMARY KEY,
                    city TEXT,
                    temperature REAL,
                    wind_speed REAL,
                    wind_direction REAL,
                    data_type TEXT CHECK(data_type IN ('A', 'P'))
                )
            """)
            
            for i in range(len(times)):
                date_str = times[i]
                t_max = temps_max[i] if i < len(temps_max) else None
                t_min = temps_min[i] if i < len(temps_min) else None
                
                if t_max is not None and t_min is not None:
                    temperature = (t_max + t_min) / 2
                else:
                    temperature = 0.0
                    
                wind_speed = winds[i] if i < len(winds) and winds[i] is not None else 0.0
                wind_direction = 0.0
                
                cursor.execute("""
                    INSERT OR REPLACE INTO weather (date, city, temperature, wind_speed, wind_direction, data_type)
                    VALUES (?, ?, ?, ?, ?, 'A')
                """, (date_str, city_name, temperature, wind_speed, wind_direction))
                
            conn.commit()
            conn.close()
            print("✅ All historical data fetched and stored instantly!")
        else:
            print("Failed to fetch data, status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    fetch_and_store_historical_data()