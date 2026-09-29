from app.services.ocr import extract_text


image_path = "sample_data/bill.JPEG"

text = extract_text(image_path)

print("\n===== OCR RESULT =====\n")
print(text)