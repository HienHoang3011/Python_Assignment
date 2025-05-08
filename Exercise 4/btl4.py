import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib

df = pd.read_csv('Exercise 4/football_data.csv', na_values=['N/a'])
df.drop(columns={'Player','Nation','Position','Team'}, inplace= True)

target = 'Transfer_Value'
features = [col for col in df.columns if col != target]

df = df[features + [target]].fillna(0)
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

rf_initial = RandomForestRegressor(n_estimators=100, random_state=42)
rf_initial.fit(X_train, y_train)
feature_importance = rf_initial.feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': feature_importance
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 8))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='skyblue')
plt.xlabel('Feature Importance')
plt.ylabel('Feature')
plt.title('Feature Importance for Transfer Value Prediction')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('Exercise 4/feature_importance_plot.png')
plt.close()

importance_threshold = 0.01
important_features = feature_importance_df[feature_importance_df['Importance'] > importance_threshold]['Feature'].tolist()

print(important_features)

X_train_selected = pd.DataFrame(X_train, columns=features)[important_features].values
X_test_selected = pd.DataFrame(X_test, columns=features)[important_features].values

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_selected, y_train)

y_pred_rf = rf_model.predict(X_test_selected)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f'Random Forest with Selected Features - MSE: {mse_rf:.2f}, R2: {r2_rf:.2f}')

model_filename = 'Exercise 4/model_predict_transfer_value_model.pkl'
print(f"Saving model to {model_filename}...")
joblib.dump(rf_model, model_filename)
print("Model saved successfully.")

