import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

print("=" * 60)
print("FOOD DELIVERY TIME PREDICTION - GRAPH ANALYSIS")
print("=" * 60)

# 1️⃣ Load Dataset (resolve path relative to this script)
BASE_DIR = Path(__file__).resolve().parent
data_path = BASE_DIR / "Dataset.csv"
if not data_path.exists():
    raise FileNotFoundError(f"Dataset file not found at {data_path}.")
df = pd.read_csv(data_path)

# Basic Cleaning
df = df.drop_duplicates()
df = df.dropna()

print("\nDataset Shape:", df.shape)

# 2️⃣ Define Features
X = df[['Distance_km']]
y = df['Delivery_Time']

# 3️⃣ Polynomial Features (Improves fit slightly)
poly = PolynomialFeatures(degree=3)
X_poly = poly.fit_transform(X)

# 4️⃣ Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_poly, y, test_size=0.2, random_state=42
)

# 5️⃣ Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# 6️⃣ Predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# 7️⃣ Evaluation
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

print("\nModel Performance:")
print("Training R2:", round(train_r2, 4))
print("Testing R2:", round(test_r2, 4))
print("Accuracy:", round(test_r2 * 100, 2), "%")
print("MAE:", round(mean_absolute_error(y_test, y_test_pred), 2))
print("RMSE:", round(np.sqrt(mean_squared_error(y_test, y_test_pred)), 2))

# ============================================================
# 📊 GRAPH 1 – Scatter Plot
# ============================================================

plt.figure()
plt.scatter(df['Distance_km'], df['Delivery_Time'])
plt.xlabel("Distance (km)")
plt.ylabel("Delivery Time (minutes)")
plt.title("Distance vs Delivery Time")
plt.show()

# ============================================================
# 📊 GRAPH 2 – Regression Line
# ============================================================

# Sort for smooth curve
sorted_idx = np.argsort(df['Distance_km'])
X_sorted = df['Distance_km'].values[sorted_idx].reshape(-1, 1)
X_sorted_poly = poly.transform(X_sorted)
y_sorted_pred = model.predict(X_sorted_poly)

plt.figure()
plt.scatter(df['Distance_km'], df['Delivery_Time'])
plt.plot(X_sorted, y_sorted_pred)
plt.xlabel("Distance (km)")
plt.ylabel("Delivery Time (minutes)")
plt.title("Polynomial Regression Fit")
plt.show()

# ============================================================
# 📊 GRAPH 3 – Residual Plot
# ============================================================

residuals = y_test - y_test_pred

plt.figure()
plt.scatter(range(len(residuals)), residuals)
plt.axhline(0)
plt.xlabel("Test Samples")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()

# Save model to script directory
joblib.dump(model, str(BASE_DIR / "delivery_model.pkl"))

print("\nMODEL TRAINED & GRAPHS GENERATED SUCCESSFULLY 🚀")
