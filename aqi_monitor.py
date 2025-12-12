import random
import time
import os

# AQI Breakpoints based on US EPA Standard
breakpoints = {
    "PM2.5": [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 500.4, 301, 500),
    ],
    "PM10": [
        (0, 54, 0, 50),
        (55, 154, 51, 100),
        (155, 254, 101, 150),
        (255, 354, 151, 200),
        (355, 424, 201, 300),
        (425, 604, 301, 500),
    ],
    "CO": [
        (0.0, 4.4, 0, 50),
        (4.5, 9.4, 51, 100),
        (9.5, 12.4, 101, 150),
        (12.5, 15.4, 151, 200),
        (15.5, 30.4, 201, 300),
        (30.5, 50.4, 301, 500),
    ],
    "SO2": [
        (0, 35, 0, 50),
        (36, 75, 51, 100),
        (76, 185, 101, 150),
        (186, 304, 151, 200),
        (305, 604, 201, 300),
        (605, 1004, 301, 500),
    ],
    "NO2": [
        (0, 53, 0, 50),
        (54, 100, 51, 100),
        (101, 360, 101, 150),
        (361, 649, 151, 200),
        (650, 1249, 201, 300),
        (1250, 2049, 301, 500),
    ],
    "O3": [
        (0.000, 0.054, 0, 50),
        (0.055, 0.070, 51, 100),
        (0.071, 0.085, 101, 150),
        (0.086, 0.105, 151, 200),
        (0.106, 0.200, 201, 300),
        (0.201, 0.604, 301, 500),
    ]
}

# Calculate AQI for one pollutant using breakpoint interpolation
def calculate_individual_aqi(cp, pollutant):
    for bp_low, bp_high, aqi_low, aqi_high in breakpoints[pollutant]:
        if bp_low <= cp <= bp_high:
            aqi = ((aqi_high - aqi_low) / (bp_high - bp_low)) * (cp - bp_low) + aqi_low
            return int(aqi)
    return 500

# AQI Category
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "Air is clean and healthy."
    elif aqi <= 100:
        return "Moderate", "Air quality is acceptable."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "Children & elderly should limit outdoor time."
    elif aqi <= 200:
        return "Unhealthy", "Avoid prolonged outdoor activities."
    elif aqi <= 300:
        return "Very Unhealthy", "Serious health risks; stay indoors."
    else:
        return "Hazardous", "Health emergency: Avoid going outside."

# IoT-style display loop
while True:
    os.system("cls" if os.name == "nt" else "clear")

    # Simulated sensor readings
    pm25 = round(random.uniform(5, 300), 2)
    pm10 = round(random.uniform(20, 400), 2)
    co = round(random.uniform(0.1, 20), 2)
    so2 = round(random.uniform(5, 300), 2)
    no2 = round(random.uniform(10, 500), 2)
    o3 = round(random.uniform(0.02, 0.20), 3)

    readings = {
        "PM2.5": pm25,
        "PM10": pm10,
        "CO": co,
        "SO2": so2,
        "NO2": no2,
        "O3": o3
    }

    # Calculate AQI for all pollutants
    aqi_values = {p: calculate_individual_aqi(v, p) for p, v in readings.items()}

    # Find dominant pollutant
    dominant_pollutant = max(aqi_values, key=aqi_values.get)
    final_aqi = aqi_values[dominant_pollutant]

    # Category & Advice
    category, message = get_aqi_category(final_aqi)

    # Display like IoT device
    print("==============================================")
    print("        🌫️  REAL-TIME IoT AQI MONITOR  🌫️      ")
    print("==============================================\n")

    for p, v in readings.items():
        print(f"{p:<6} : {v:<10} → AQI: {aqi_values[p]}")

    print("\n----------------------------------------------")
    print(f" Dominant Pollutant : {dominant_pollutant}")
    print(f" Final AQI          : {final_aqi}")
    print(f" Category           : {category}")
    print(f" Health Message     : {message}")
    print("----------------------------------------------\n")

    time.sleep(3)
