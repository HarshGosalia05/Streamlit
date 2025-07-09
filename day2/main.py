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

    },

    "winter" : {
        'irradiance': (300, 700),
        'humidity': (30, 70),
        'wind_speed': (1, 6),
        'ambient_temperature': (5, 20),
        'tilt_angle': (10, 40)
    },

    'monsoon': {
        'irradiance': (100, 600),
        'humidity': (70, 100),
        'wind_speed': (2, 8),
        'ambient_temperature': (20, 35),
        'tilt_angle': (10, 40),
    }   

}

summer_months_day = {
    'March' : 31,
    'April' : 30,
    'May' : 31,
    'June' : 30
}

winter_months_day = {
    'November': 30,
    'December': 31,
    'January': 31,
    'February': 28  
}

monsoon_months_days = {
    'July': 31,
    'August': 31,
    'September': 30,
    'October': 31
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




df_summer = generate_summer_data_by_month(feature_ranges,summer_months_day)
print("\n\nSummer Data\n")
# print(df_summer)

df_winter = ganerate_winter_data_bt_month(feature_ranges,winter_months_day)
print("\n\Winter Data\n")
# print(df_winter)

df_monsoon = generate_monsoon_data_by_month(feature_ranges, monsoon_months_days)
print("\n\nMonsoon Data\n")
# print(df_monsoon)



# Concatenate summer, winter, and monsoon dataframes
df_all_seasons = pd.concat([df_summer, df_winter, df_monsoon], ignore_index=True)

# Show first few rows to verify
print("\n\n")
print(df_all_seasons.head())

# Print dataset info
print("\n\n")
df_all_seasons.info()

# Optionally save to CSV
print("\n\n")
df_all_seasons.to_csv('solar_performance_all_seasons.csv', index=False)



import matplotlib.pyplot as plt

# Boxplot of kWh by season
plt.figure(figsize=(8,6))
df_all_seasons.boxplot(column='kwh', by='season', grid=False)
plt.title('Solar Panel Energy Output (kWh) by Season')
plt.suptitle('')  # Remove automatic subtitle
plt.xlabel('Season')
plt.ylabel('Energy Output (kWh)')
plt.show()





# Plotting kWh for each row (day) using index as x-axis
plt.figure(figsize=(14,6))
plt.bar(df_all_seasons.index, df_all_seasons['kwh'], color='orange')

plt.xlabel('Day Index')
plt.ylabel('Energy Output (kWh)')
plt.title('Day-wise Solar Panel Energy Output (Unaveraged)')
plt.tight_layout()
plt.show()







# import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Load your CSV file
df = pd.read_csv("D:\werkshop\solar_performance_all_seasons.csv")  # Replace with your actual filename

# Step 2: Define features (X) and target (y)
X = df[['irradiance', 'humidity', 'wind_speed', 'ambient_temperature', 'tilt_angle']]
y = df['kwh']

# Step 3: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# print(df)
# print(df.head())





# Step 4: Create and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Make predictions
y_pred = model.predict(X_test)

# Step 6: Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Step 7: Print model details and evaluation
print("Model Coefficients:", model.coef_)
print("Intercept:", model.intercept_)
print("Mean Squared Error (MSE):", mse)
print("R² Score:", r2)

# import matplotlib.pyplot as plt
import seaborn as sns

# 1. Scatter plot: Actual vs. Predicted
plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=y_pred)
plt.xlabel("Actual kWh")
plt.ylabel("Predicted kWh")
plt.title("Actual vs. Predicted kWh")
plt.plot([y_test.min(), y_test.max()], [y_pred.min(), y_pred.max()], 'r--')  # Diagonal line red dash line
plt.grid(True)
plt.show()









import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import   classification_report, accuracy_score

# Step 1: Load the CSV (replace with your real filename)
df = pd.read_csv("/content/solar_performance_all_seasons.csv")  # Update with actual path

# Step 2: Define features (X) and target (y)
X = df[['irradiance', 'humidity', 'wind_speed', 'ambient_temperature', 'tilt_angle','kwh']]
y = df['season']

# Step 3: Encode the categorical target into numeric labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)  # e.g., summer -> 2, winter -> 1, etc.

# Step 4: Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)



print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)











# Step 5: Train Logistic Regression model
model = LogisticRegression(max_iter=10)
model.fit(X_train, y_train)

# Step 6: Make predictions
y_pred = model.predict(X_test)

# Step 7: Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))    






from sklearn.metrics import confusion_matrix
# Step 8: Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()