import pandas as pd
import numpy as np
import pandas

feature_range = {
    "winter" : {
        'irradiance': (300, 700),
        'humidity': (30, 70),
        'wind_speed': (1, 6),
        'ambient_temperature': (5, 20),
        'tilt_angle': (10, 40)
    }
}

winter_months_day = {
    'November': 30,
    'December': 31,
    'January': 31,
    'February': 28  
}


def cal_kwh_winter(irr,hum,win,temp,ang):
    return ( 0.25 * irr - 0.025*hum + 0.02*win + 0.1*temp - 0.03 * abs(ang-30)) 


def ganerate_winter_data_bt_month(feature_range,months_day):
    data = []
    for month,day in months_day.items():
        for _ in range(day):
            irr = np.random.uniform(*feature_range["winter"]["irradiance"])
            hum = np.random.uniform(*feature_range["winter"]["humidity"])
            win = np.random.uniform(*feature_range["winter"]["wind_speed"])
            temp = np.random.uniform(*feature_range["winter"]["ambient_temperature"])
            ang = np.random.uniform(*feature_range["winter"]["tilt_angle"])

            kwh = cal_kwh_winter(irr,hum,win,temp,ang)

            data.append({
                'irradiance' : round(irr,2),
                'humidity' : round(hum,2),
                'wind_speed' : round(win,2),
                'ambient_temperature' : round(temp,2),
                'tilt_angle' :round(ang,2),
                'kwh' : round(kwh,2),
                'season' : 'winter',
                'month' : month


            })
    return pd.DataFrame(data)


    


df_winter = ganerate_winter_data_bt_month(feature_range,winter_months_day)
print(df_winter)