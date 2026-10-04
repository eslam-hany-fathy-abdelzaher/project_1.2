import requests

# كمثال سريع بدون مفتاح معقد Open-Meteo مثلاً لمدينة نيويورك باستخدام رابط تجريبي لبيانات الطقس #
url = "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current=temperature_2m,wind_speed_10m"

try:
    # إرسال طلب HTTP GET للـ API #
    response = requests.get(url)
    
    # فحص حالة الطلب (لو 200 يبقى تمام وشغال) #
    if response.status_code == 200:
        data = response.json()
        print("Data fetched successfully!")
        print("Current Temperature in New York:", data['current']['temperature_2m'], "°C")
        print("Wind Speed:", data['current']['wind_speed_10m'], "km/h")
    else:
        print("Connection failed, status code:", response.status_code)

except Exception as e:
    print("An error occurred:", e)