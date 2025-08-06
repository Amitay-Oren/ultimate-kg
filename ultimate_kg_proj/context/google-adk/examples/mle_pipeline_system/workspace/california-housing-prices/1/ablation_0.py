
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Load the training data
train_data = pd.read_csv("./input/train.csv")

# Separate features and target variable from the training data
X = train_data.drop("median_house_value", axis=1)
y = train_data["median_house_value"]

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=0)

# --- Baseline Model ---
# Handle missing values using imputation
imputer = SimpleImputer(strategy="median")
X_train_imputed = imputer.fit_transform(X_train)
X_val_imputed = imputer.transform(X_val)

# Train the Gradient Boosting Regressor model
gbr = GradientBoostingRegressor(n_estimators=100, random_state=0)
gbr.fit(X_train_imputed, y_train)

# Make predictions on the validation set
y_pred_val = gbr.predict(X_val_imputed)

# Evaluate the model on the validation data
rmse_val = np.sqrt(mean_squared_error(y_val, y_pred_val))
print(f"Baseline RMSE on the validation data: {rmse_val}")

baseline_rmse = rmse_val

# --- Ablation 1: No Imputation ---
X_train_no_impute = X_train.fillna(0)
X_val_no_impute = X_val.fillna(0)

gbr_no_impute = GradientBoostingRegressor(n_estimators=100, random_state=0)
gbr_no_impute.fit(X_train_no_impute, y_train)

y_pred_val_no_impute = gbr_no_impute.predict(X_val_no_impute)
rmse_val_no_impute = np.sqrt(mean_squared_error(y_val, y_pred_val_no_impute))
print(f"Ablation 1 (No Imputation) RMSE on the validation data: {rmse_val_no_impute}")

# --- Ablation 2: Fewer Estimators ---
# Handle missing values using imputation
imputer = SimpleImputer(strategy="median")
X_train_imputed = imputer.fit_transform(X_train)
X_val_imputed = imputer.transform(X_val)

gbr_fewer_estimators = GradientBoostingRegressor(n_estimators=50, random_state=0)
gbr_fewer_estimators.fit(X_train_imputed, y_train)

# Make predictions on the validation set
y_pred_val_fewer_estimators = gbr_fewer_estimators.predict(X_val_imputed)

# Evaluate the model on the validation data
rmse_val_fewer_estimators = np.sqrt(mean_squared_error(y_val, y_pred_val_fewer_estimators))
print(f"Ablation 2 (Fewer Estimators) RMSE on the validation data: {rmse_val_fewer_estimators}")

print("\n--- Ablation Study Results ---")
print(f"Baseline RMSE: {baseline_rmse}")
print(f"Ablation 1 (No Imputation) RMSE: {rmse_val_no_impute}")
print(f"Ablation 2 (Fewer Estimators) RMSE: {rmse_val_fewer_estimators}")

if rmse_val_no_impute > baseline_rmse:
    print("Imputation contributes to the overall performance.")
else:
    print("Imputation does not contribute to the overall performance.")

if rmse_val_fewer_estimators > baseline_rmse:
    print("Number of Estimators contributes to the overall performance.")
else:
    print("Number of Estimators does not contribute to the overall performance.")
