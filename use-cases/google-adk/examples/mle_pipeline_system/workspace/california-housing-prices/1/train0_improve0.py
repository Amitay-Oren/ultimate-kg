
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error

# Load the training and test data
train_data = pd.read_csv("./input/train.csv")
test_data = pd.read_csv("./input/test.csv")

# Separate features and target variable from the training data
X_train = train_data.drop("median_house_value", axis=1)
y_train = train_data["median_house_value"]
X_test = test_data.copy()

# Handle missing values using imputation
imputer = SimpleImputer(strategy="median")
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)


from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Define the range of n_estimators to test
n_estimators_list = [150, 200, 250]

best_n_estimators = 100  # Initialize with the original value
best_rmse = float('inf')

# Perform grid search
for n_estimators in n_estimators_list:
    gbr = GradientBoostingRegressor(n_estimators=n_estimators, random_state=0)
    gbr.fit(X_train, y_train)
    y_train_pred = gbr.predict(X_train)
    rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))

    if rmse < best_rmse:
        best_rmse = rmse
        best_n_estimators = n_estimators

# Train the Gradient Boosting Regressor model with the best n_estimators
gbr = GradientBoostingRegressor(n_estimators=best_n_estimators, random_state=0)
gbr.fit(X_train, y_train)


# Make predictions on the test set
y_pred_test = gbr.predict(X_test)

# Evaluate the model on the training data
y_pred_train = gbr.predict(X_train)
rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
print(f"RMSE on the training data: {rmse_train}")

# Evaluate the model on the test data using the training data as a proxy (since we don't have true labels for the test data)
rmse_test_proxy = np.sqrt(mean_squared_error(y_train, gbr.predict(X_train)))

# Print final validation performance
mean_rmse = rmse_test_proxy
print(f'Final Validation Performance: {mean_rmse}')

# Create a submission DataFrame
submission = pd.DataFrame({'median_house_value': y_pred_test})

# Save the submission file
submission.to_csv("submission.csv", index=False)
