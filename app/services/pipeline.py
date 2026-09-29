from app.services.ocr import extract_text
from app.services.extraction import extract_bill_fields
from app.services.validation import validate_bill
from app.services.anomaly import detect_anomaly


def analyze_bill(image_path: str):

    # Step 1: OCR
    raw_text = extract_text(image_path)

    # Step 2: Extract structured fields
    bill_data = extract_bill_fields(raw_text)

    # Step 3: Validate extracted data
    validation_result = validate_bill(bill_data)

    # Step 4: Prepare data for anomaly detection
    anomaly_input = {
        "total_amount": bill_data.get("total_amount"),
        "gst_amount": bill_data.get("gst_amount"),
        "discount": bill_data.get("discount"),
        "payable_amount": bill_data.get("payable_amount"),
        "received_amount": bill_data.get("received_amount"),
        "item_count": bill_data.get("item_count", 0),
    }

    anomaly_result = detect_anomaly(anomaly_input)

    return {
        "bill_data": bill_data,
        "validation": validation_result,
        "anomaly": anomaly_result,
       
    }


if __name__ == "__main__":

    image_path = "sample_data/bill.jpeg"

    result = analyze_bill(image_path)

    print("\n===== BILL ANALYSIS =====\n")

    print("BILL DATA:")
    print(result["bill_data"])

    print("\nVALIDATION:")
    print(result["validation"])

    print("\nANOMALY:")
    print(result["anomaly"])