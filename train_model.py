import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load dataset
df = pd.read_csv("Dataset.csv")

print("Available Columns:")
print(df.columns)

# Automatically detect target column
target_column = None
for col in df.columns:
    if "time" in col.lower():
        target_column = col
        break

if target_column is None:
    raise Exception("Target column not found!")

print("Detected Target Column:", target_column)

# Drop unwanted columns
for col in ["ID", "Delivery_person_ID"]:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

# Define X and y
X = df.drop(target_column, axis=1)
y = df[target_column]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Optimized RandomForest
model = RandomForestRegressor(
    n_estimators=120,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))

print("MAE:", mae)
print("RMSE:", rmse)

# Save model
joblib.dump(model, "delivery_model.pkl")

print("Model trained and saved successfully!")
