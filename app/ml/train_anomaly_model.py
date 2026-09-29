import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest


# 1. Load dataset
df = pd.read_csv("sample_data/invoices.csv")


# 2. Select features
features = [
    "total_amount",
    "gst_amount",
    "discount",
    "payable_amount",
    "received_amount",
    "item_count"
]

X = df[features]


# 3. Create model
model = IsolationForest(
    n_estimators=200,
    contamination=0.04,
    random_state=42
)


# 4. Train model
model.fit(X)


# 5. Save trained model
joblib.dump(
    model,
    "app/ml/anomaly_model.pkl"
)


print("Anomaly detection model trained successfully.")
print("Training samples:", len(X))
print("Features:", features)
print("Model saved to: app/ml/anomaly_model.pkl")