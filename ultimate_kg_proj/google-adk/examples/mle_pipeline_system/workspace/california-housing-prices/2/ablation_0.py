
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the training data
train_data = pd.read_csv("./input/train.csv")

# Handle missing values with mean imputation
train_data = train_data.fillna(train_data.mean())

# Extract features and target from the training data
features = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']
target = 'median_house_value'

X_train = train_data[features]
y_train = train_data[target]

# Split the training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# --- Ablation 1: Removing 'housing_median_age' feature ---
print("Ablation 1: Removing 'housing_median_age' feature")
features_ablation_1 = ['longitude', 'latitude', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']
X_train_ablation_1 = X_train[features_ablation_1]
X_val_ablation_1 = X_val[features_ablation_1]

params = {'n_estimators': 500, 'max_depth': 5, 'min_samples_split': 2,
          'min_samples_leaf': 1, 'learning_rate': 0.01, 'loss': 'squared_error'}
model_ablation_1 = GradientBoostingRegressor(**params)
model_ablation_1.fit(X_train_ablation_1, y_train)
mse_ablation_1 = mean_squared_error(y_val, model_ablation_1.predict(X_val_ablation_1))
rmse_ablation_1 = np.sqrt(mse_ablation_1)
print("Validation RMSE (Ablation 1): %.4f" % rmse_ablation_1)

# --- Ablation 2: Reducing n_estimators to 200 ---
print("\nAblation 2: Reducing n_estimators to 200")
X_train_ablation_2 = X_train[features]
X_val_ablation_2 = X_val[features]

params_ablation_2 = {'n_estimators': 200, 'max_depth': 5, 'min_samples_split': 2,
          'min_samples_leaf': 1, 'learning_rate': 0.01, 'loss': 'squared_error'}
model_ablation_2 = GradientBoostingRegressor(**params_ablation_2)
model_ablation_2.fit(X_train_ablation_2, y_train)
mse_ablation_2 = mean_squared_error(y_val, model_ablation_2.predict(X_val_ablation_2))
rmse_ablation_2 = np.sqrt(mse_ablation_2)
print("Validation RMSE (Ablation 2): %.4f" % rmse_ablation_2)

# --- Original Model ---
print("\nOriginal Model")
params = {'n_estimators': 500, 'max_depth': 5, 'min_samples_split': 2,
          'min_samples_leaf': 1, 'learning_rate': 0.01, 'loss': 'squared_error'}
model = GradientBoostingRegressor(**params)

model.fit(X_train, y_train)

# Evaluate the model on the validation set
mse = mean_squared_error(y_val, model.predict(X_val))
rmse = np.sqrt(mse)
print("Validation RMSE (Original): %.4f" % rmse)

print("\nConclusion:")
if rmse_ablation_1 < rmse and rmse_ablation_1 < rmse_ablation_2:
    print("Removing 'housing_median_age' improved the model performance.")
elif rmse_ablation_2 < rmse and rmse_ablation_2 < rmse_ablation_1:
    print("Reducing n_estimators to 200 improved the model performance.")
else:
    print("The original model performs the best.")
