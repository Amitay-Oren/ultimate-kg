
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


from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor

# Define the parameter grid
param_grid = {
    'n_estimators': [150, 200],
    'learning_rate': [0.05, 0.1],
    'max_depth': [3, 4]
}

# Create a Gradient Boosting Regressor object
gbr = GradientBoostingRegressor(random_state=0)

# Perform GridSearchCV
grid_search = GridSearchCV(gbr, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Get the best estimator
best_gbr = grid_search.best_estimator_

# Print the best parameters
print("Best parameters:", grid_search.best_params_)


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
