
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load the training and test data
train_data = pd.read_csv("./input/train.csv")
test_data = pd.read_csv("./input/test.csv")

# Separate features and target variable from the training data
X = train_data.drop("median_house_value", axis=1)
y = train_data["median_house_value"]

# Handle missing values using imputation
imputer = SimpleImputer(strategy="median")
X = pd.DataFrame(imputer.fit_transform(X), columns = X.columns)
test_data = pd.DataFrame(imputer.transform(test_data), columns = test_data.columns)

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

X_test = test_data.copy()

# Train the Gradient Boosting Regressor model
gbr = GradientBoostingRegressor(n_estimators=100, random_state=0)
gbr.fit(X_train, y_train)

# Train the Random Forest Regressor model
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Make predictions on the validation set
y_pred_val_gbr = gbr.predict(X_val)
y_pred_val_rf = rf.predict(X_val)

# Evaluate the models on the validation set
rmse_val_gbr = np.sqrt(mean_squared_error(y_val, y_pred_val_gbr))
rmse_val_rf = np.sqrt(mean_squared_error(y_val, y_pred_val_rf))

print(f"RMSE on the validation data (GBR): {rmse_val_gbr}")
print(f"RMSE on the validation data (RF): {rmse_val_rf}")

# Ensemble the predictions using a simple average
y_pred_val_ensemble = (y_pred_val_gbr + y_pred_val_rf) / 2
rmse_val_ensemble = np.sqrt(mean_squared_error(y_val, y_pred_val_ensemble))
print(f"RMSE on the validation data (Ensemble): {rmse_val_ensemble}")

# Make predictions on the test set
y_pred_test_gbr = gbr.predict(X_test)
y_pred_test_rf = rf.predict(X_test)

# Ensemble the test set predictions
y_pred_test_ensemble = (y_pred_test_gbr + y_pred_test_rf) / 2

# Print final validation performance
mean_rmse = rmse_val_ensemble
print(f'Final Validation Performance: {mean_rmse}')

# Create a submission DataFrame
submission = pd.DataFrame({'median_house_value': y_pred_test_ensemble})

# Save the submission file
submission.to_csv("submission.csv", index=False)
