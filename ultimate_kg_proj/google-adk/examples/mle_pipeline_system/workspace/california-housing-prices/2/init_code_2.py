
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the training and testing data
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

# Subsample the training data
subsample_size = 0.5  # Reduced subsample size
X_train_subsampled = X_train.sample(frac=subsample_size, random_state=42)
y_train_subsampled = y_train.loc[X_train_subsampled.index]

# Train a Gradient Boosting Regressor model
params = {'n_estimators': 100, 'max_depth': 5, 'min_samples_split': 2,
          'min_samples_leaf': 1, 'learning_rate': 0.1, 'loss': 'squared_error'}
model = GradientBoostingRegressor(**params)

model.fit(X_train_subsampled, y_train_subsampled)

# Make predictions on the validation set
y_pred_val = model.predict(X_val)

# Evaluate the model on the validation set
rmse = np.sqrt(mean_squared_error(y_val, y_pred_val))
print(f"Validation RMSE: {rmse}")

# Train the model on the full training data
model.fit(X_train, y_train)

# Make predictions on the test data
X_test = test_data[features]
y_pred_test = model.predict(X_test)

# Save the predictions to a CSV file
output = pd.DataFrame({'median_house_value': y_pred_test})
output.to_csv('submission.csv', index=False)

final_validation_score = rmse
print(f"Final Validation Performance: {final_validation_score}")
