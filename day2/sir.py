import numpy as np

feature_ranges = {
    'winter': {
        'irradiance': (300, 700),
        'humidity': (30, 70),
        'wind_speed': (1, 6),
        'ambient_temperature': (5, 20),
        'tilt_angle': (10, 40),
    }
}

# Winter months with exact days
winter_months_days = {
    'November': 30,
    'December': 31,
    'January': 31,
    'February': 28  # Not considering leap year here; can be adjusted if needed
}

def calc_kwh_winter(irradiance, humidity, wind_speed, ambient_temp, tilt_angle):
    return (0.18 * irradiance
            - 0.03 * humidity
            + 0.015 * wind_speed
            + 0.08 * ambient_temp
            - 0.02 * abs(tilt_angle - 30))

def generate_winter_data_by_month(feature_ranges, months_days):
    data = []
    for month, days in months_days.items():
        for _ in range(days):
            irr = np.random.uniform(*feature_ranges['winter']['irradiance'])
            hum = np.random.uniform(*feature_ranges['winter']['humidity'])
            wind = np.random.uniform(*feature_ranges['winter']['wind_speed'])
            temp = np.random.uniform(*feature_ranges['winter']['ambient_temperature'])
            tilt = np.random.uniform(*feature_ranges['winter']['tilt_angle'])
            
            kwh = calc_kwh_winter(irr, hum, wind, temp, tilt)

            data.append({
                'irradiance': round(irr, 2),
                'humidity': round(hum, 2),
                'wind_speed': round(wind, 2),
                'ambient_temperature': round(temp, 2),
                'tilt_angle': round(tilt, 2),
                'kwh': round(kwh, 2),
                'season': 'winter',
                'month': month
            })
    return pd.DataFrame(data)

# Generate winter data matching days in each month
df_winter = generate_winter_data_by_month(feature_ranges, winter_months_days)

print(df_winter.head())
print(f'Total winter data points generated: {len(df_winter)}')  # Should be 31+31+28=90






# Concatenate summer, winter, and monsoon dataframes
df_all_seasons = pd.concat([df_summer, df_winter, df_monsoon], ignore_index=True)

# Show first few rows to verify
print(df_all_seasons.head())

# Print dataset info
df_all_seasons.info()

# Optionally save to CSV
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



import matplotlib.pyplot as plt

# Plotting kWh for each row (day) using index as x-axis
plt.figure(figsize=(14,6))
plt.bar(df_all_seasons.index, df_all_seasons['kwh'], color='orange')

plt.xlabel('Day Index')
plt.ylabel('Energy Output (kWh)')
plt.title('Day-wise Solar Panel Energy Output (Unaveraged)')
plt.tight_layout()
plt.show()




import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Load your CSV file
df = pd.read_csv("/content/solar_performance_all_seasons.csv")  # Replace with your actual filename

# Step 2: Define features (X) and target (y)
X = df[['irradiance', 'humidity', 'wind_speed', 'ambient_temperature', 'tilt_angle']]
y = df['kwh']

# Step 3: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)



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



import matplotlib.pyplot as plt
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

























































# import numpy as np
# import pandas as pd

# feature_ranges = {
#     'winter': {
#         'irradiance': (300, 700),
#         'humidity': (30, 70),
#         'wind_speed': (1, 6),
#         'ambient_temperature': (5, 20),
#         'tilt_angle': (10, 40),
#     }
# }

# # Winter months with exact days
# winter_months_days = {
#     'November': 30,
#     'December': 31,
#     'January': 31,
#     'February': 28  # Not considering leap year here; can be adjusted if needed
# }

# def calc_kwh_winter(irradiance, humidity, wind_speed, ambient_temp, tilt_angle):
#     return (0.18 * irradiance
#             - 0.03 * humidity
#             + 0.015 * wind_speed
#             + 0.08 * ambient_temp
#             - 0.02 * abs(tilt_angle - 30))

# def generate_winter_data_by_month(feature_ranges, months_days):
#     data = []
#     for month, days in months_days.items():
#         for _ in range(days):
#             irr = np.random.uniform(*feature_ranges['winter']['irradiance'])
#             hum = np.random.uniform(*feature_ranges['winter']['humidity'])
#             wind = np.random.uniform(*feature_ranges['winter']['wind_speed'])
#             temp = np.random.uniform(*feature_ranges['winter']['ambient_temperature'])
#             tilt = np.random.uniform(*feature_ranges['winter']['tilt_angle'])
            
#             kwh = calc_kwh_winter(irr, hum, wind, temp, tilt)

#             data.append({
#                 'irradiance': round(irr, 2),
#                 'humidity': round(hum, 2),
#                 'wind_speed': round(wind, 2),
#                 'ambient_temperature': round(temp, 2),
#                 'tilt_angle': round(tilt, 2),
#                 'kwh': round(kwh, 2),
#                 'season': 'winter',
#                 'month': month
#             })
#     return pd.DataFrame(data)

# # Generate winter data matching days in each month
# df_winter = generate_winter_data_by_month(feature_ranges, winter_months_days)

# print(df_winter.head())
# print(f'Total winter data points generated: {len(df_winter)}')  # Should be 31+31+28=90
