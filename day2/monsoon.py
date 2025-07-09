import numpy as np
import pandas as pd

feature_ranges = {
    'monsoon': {
        'irradiance': (100, 600),
        'humidity': (70, 100),
        'wind_speed': (2, 8),
        'ambient_temperature': (20, 35),
        'tilt_angle': (10, 40),
    }
}

# Monsoon months with exact days
monsoon_months_days = {
    'July': 31,
    'August': 31,
    'September': 30,
    'October': 31
}

def calc_kwh_monsoon(irradiance, humidity, wind_speed, ambient_temp, tilt_angle):
    return (0.15 * irradiance
            - 0.1 * humidity
            + 0.01 * wind_speed
            + 0.05 * ambient_temp
            - 0.04 * abs(tilt_angle - 30))

def generate_monsoon_data_by_month(feature_ranges, months_days):
    data = []
    for month, days in months_days.items():
        for _ in range(days):
            irr = np.random.uniform(*feature_ranges['monsoon']['irradiance'])
            hum = np.random.uniform(*feature_ranges['monsoon']['humidity'])
            wind = np.random.uniform(*feature_ranges['monsoon']['wind_speed'])
            temp = np.random.uniform(*feature_ranges['monsoon']['ambient_temperature'])
            tilt = np.random.uniform(*feature_ranges['monsoon']['tilt_angle'])

            kwh = calc_kwh_monsoon(irr, hum, wind, temp, tilt)

            data.append({
                'irradiance': round(irr, 2),
                'humidity': round(hum, 2),
                'wind_speed': round(wind, 2),
                'ambient_temperature': round(temp, 2),
                'tilt_angle': round(tilt, 2),
                'kwh': round(kwh, 2),
                'season': 'monsoon',
                'month': month
            })
    return pd.DataFrame(data)

# Generate monsoon data matching days in each month
df_monsoon = generate_monsoon_data_by_month(feature_ranges, monsoon_months_days)

print(df_monsoon.head())
print(f'Total monsoon data points generated: {len(df_monsoon)}')