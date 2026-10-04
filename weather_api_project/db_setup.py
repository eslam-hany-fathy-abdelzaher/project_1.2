import sqlite3

def create_database():
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

    conn.commit()
    conn.close()
    print("✅ Database and table created successfully!")

if __name__ == "__main__":
    create_database()