import pandas as pd
import numpy as np
import random 

feature_ranges  = {
     "summer" : {
            "irradiance" : (600,1000),
            "humidity" : (10,50),
            "wind_speed" : (0,5),
            "ambient_temperature" : (10,40),
            'tilt_angle': (10, 40)

    }
}

summer_months_day = {
    'March' : 31,
    'April' : 30,
    'May' : 31,
    'June' : 30
}



def cal_kwh_summer(irr,hum,ws,at,tilt):
    return (0.25 * irr
            - 0.05 * hum
            + 0.02 * ws
            + 0.1 * at
            - 0.03 * abs(tilt - 30))

def generate_summer_data_by_month(feature_ranges,months_day):
    data = []
    for month,days in months_day.items():
        for _ in range(days):
            irr = np.random.uniform(*feature_ranges["summer"]["irradiance"])
            hum = np.random.uniform(*feature_ranges["summer"]["humidity"])
            wind = np.random.uniform(*feature_ranges["summer"]["wind_speed"])
            temp = np.random.uniform(*feature_ranges["summer"]["ambient_temperature"])
            tilt = np.random.uniform(*feature_ranges['summer']['tilt_angle'])

            kwh = cal_kwh_summer(irr,hum,wind,temp,tilt) 

            data.append({
                    'irradiance': round(irr, 2),
                    'humidity': round(hum, 2),
                    'wind_speed': round(wind, 2),
                    'ambient_temperature': round(temp, 2),
                    'tilt_angle': round(tilt, 2),
                    'kwh': round(kwh, 2),
                    'season': 'summer',
                    'month': month
                })
    return pd.DataFrame(data)
        

df_summer = generate_summer_data_by_month(feature_ranges,summer_months_day)
print(df_summer)