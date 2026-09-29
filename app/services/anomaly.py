import joblib
import pandas as pd


MODEL_PATH = "app/ml/anomaly_model.pkl"

model = joblib.load(MODEL_PATH)


def detect_anomaly(data: dict):

    features = [
        "total_amount",
        "gst_amount",
        "discount",
        "payable_amount",
        "received_amount",
        "item_count"
    ]

    input_data = pd.DataFrame(
        [[data.get(feature, 0) for feature in features]],
        columns=features
    )

    prediction = model.predict(input_data)[0]

    score = model.decision_function(input_data)[0]

    if prediction == -1:
        status = "anomaly"
    else:
        status = "normal"

    return {
        "status": status,
        "anomaly_score": round(float(score), 4)
    }
    
if __name__ == "__main__":

    normal_bill = {
        "total_amount": 850.00,
        "gst_amount": 153.00,
        "discount": 20.00,
        "payable_amount": 983.00,
        "received_amount": 983.00,
        "item_count": 4
    }

    unusual_bill = {
        "total_amount": 150000.00,
        "gst_amount": 50000.00,
        "discount": 80000.00,
        "payable_amount": 120000.00,
        "received_amount": 30000.00,
        "item_count": 75
    }

    print("\n===== NORMAL BILL =====")
    print(detect_anomaly(normal_bill))

    print("\n===== UNUSUAL BILL =====")
    print(detect_anomaly(unusual_bill))