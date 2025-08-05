
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the data
train_data = pd.read_csv("./input/train.csv")

# Handle missing values (if any)
train_data = train_data.dropna()

# Separate features and target
X = train_data.drop("median_house_value", axis=1)
y = train_data["median_house_value"]

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Try importing and using CatBoost, if it fails, use a RandomForestRegressor
try:
    from catboost import CatBoostRegressor
    model = CatBoostRegressor(iterations=100,
                                 learning_rate=0.05,
                                 depth=6,
                                 loss_function='RMSE',
                                 eval_metric='RMSE',
                                 random_seed=42,
                                 verbose=0)

    model.fit(X_train, y_train, eval_set=(X_val, y_val), early_stopping_rounds=10, verbose=0)

    # Make predictions on the validation set
    y_pred_val = model.predict(X_val)

    # Evaluate the model
    rmse = np.sqrt(mean_squared_error(y_val, y_pred_val))

    print(f'Final Validation Performance: {rmse}')
except ImportError:
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred_val = model.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred_val))
    print(f'Final Validation Performance: {rmse}')


# Prepare submission file
test_data = pd.read_csv("./input/test.csv")

# Handle missing values (if any)
test_data = test_data.dropna()

# Make predictions on the test data
y_pred_test = model.predict(test_data)

# Create submission DataFrame
submission = pd.DataFrame({'median_house_value': y_pred_test})

# Save the submission file
submission.to_csv("submission.csv", index=False)
