
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the training and test data
train_data = pd.read_csv("./input/train.csv")
test_data = pd.read_csv("./input/test.csv")

# Handle missing values with mean imputation
train_data = train_data.fillna(train_data.mean())
test_data = test_data.fillna(test_data.mean())

# Extract features and target from the training data
features = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income']
target = 'median_house_value'

X_train = train_data[features]
y_train = train_data[target]

# Split the training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Subsample the training data for the second model
subsample_size = 0.5
X_train_subsampled = X_train.sample(frac=subsample_size, random_state=42)
y_train_subsampled = y_train.loc[X_train_subsampled.index]

# Train the first Gradient Boosting Regressor model
params1 = {'n_estimators': 500, 'max_depth': 5, 'min_samples_split': 2,
          'min_samples_leaf': 1, 'learning_rate': 0.01, 'loss': 'squared_error'}
model1 = GradientBoostingRegressor(**params1)
model1.fit(X_train, y_train)

# Train the second Gradient Boosting Regressor model on subsampled data
params2 = {'n_estimators': 100, 'max_depth': 5, 'min_samples_split': 2,
          'min_samples_leaf': 1, 'learning_rate': 0.1, 'loss': 'squared_error'}
model2 = GradientBoostingRegressor(**params2)
model2.fit(X_train_subsampled, y_train_subsampled)

# Make predictions on the validation set
y_pred_val_1 = model1.predict(X_val)
y_pred_val_2 = model2.predict(X_val)

# Ensemble the predictions using a simple average
y_pred_val_ensemble = (y_pred_val_1 + y_pred_val_2) / 2

# Evaluate the ensemble model on the validation set
rmse = np.sqrt(mean_squared_error(y_val, y_pred_val_ensemble))
print(f"Validation RMSE: {rmse}")

# Make predictions on the test data using the ensemble
test_predictions_1 = model1.predict(test_data[features])
test_predictions_2 = model2.predict(test_data[features])
test_predictions_ensemble = (test_predictions_1 + test_predictions_2) / 2

# Ensure predictions are within a reasonable range
test_predictions_ensemble = np.clip(test_predictions_ensemble, 0, 500000)

# Prepare the submission file
submission = pd.DataFrame({'median_house_value': test_predictions_ensemble})

# Save the submission file
submission.to_csv('submission.csv', index=False)

final_validation_score = rmse
print(f"Final Validation Performance: {final_validation_score}")
