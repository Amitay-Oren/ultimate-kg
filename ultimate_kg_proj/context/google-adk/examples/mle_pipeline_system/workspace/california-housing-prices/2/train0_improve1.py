
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

# Create interaction features
X_train['age_income'] = X_train['housing_median_age'] * X_train['median_income']
X_train['age_population'] = X_train['housing_median_age'] * X_train['population']


y_train = train_data[target]


# Split the training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Train a Gradient Boosting Regressor model
params = {'n_estimators': 500, 'max_depth': 5, 'min_samples_split': 2,
          'min_samples_leaf': 1, 'learning_rate': 0.01, 'loss': 'squared_error'}
model = GradientBoostingRegressor(**params)

model.fit(X_train, y_train)

# Evaluate the model on the validation set
mse = mean_squared_error(y_val, model.predict(X_val))
rmse = np.sqrt(mse)
print("Validation RMSE: %.4f" % rmse)

# Make predictions on the test data
test_predictions = model.predict(test_data[features])

# Ensure predictions are within a reasonable range
test_predictions = np.clip(test_predictions, 0, 500000)

# Prepare the submission file
submission = pd.DataFrame({'median_house_value': test_predictions})

# Save the submission file
submission.to_csv('submission.csv', index=False)

final_validation_score = rmse
print(f'Final Validation Performance: {final_validation_score}')
