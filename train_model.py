import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


from pathlib import Path

# =========================
# LOAD DATA
# =========================

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "Dataset.csv")

print("Available Columns:")
print(df.columns)

# Detect target column automatically
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

# =========================
# SELECT ONLY IMPORTANT FEATURES
# =========================

features = [
    "Delivery_person_Age",
    "Delivery_person_Ratings",
    "Type_of_vehicle",
    "Type_of_order",
    "Distance_km"
]

X = df[features]
y = df[target_column]

print("\nTraining Features Used:")
print(X.columns)

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# MODEL
# =========================

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

# =========================
# METRICS
# =========================

mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = model.score(X_test, y_test)

print("\n===== MODEL PERFORMANCE =====")
print("MAE:", mae)
print("RMSE:", rmse)
print("R²:", r2)

# =========================
# SAVE MODEL + FEATURE LIST
# =========================

joblib.dump(model, BASE_DIR / "delivery_model.pkl")
joblib.dump(features, BASE_DIR / "model_features.pkl")

print("\nModel and feature list saved successfully!")
