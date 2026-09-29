
# BillAI — Intelligent Invoice & Bill Analyzer

BillAI is an AI-powered invoice and bill analysis platform that converts invoice images into structured financial information using OCR, validates extracted values, and detects potentially unusual bills using machine learning.

The application is built as a FastAPI backend with a lightweight web interface and SQLite persistence, and is containerized with Docker for deployment.

---

## 🚀 Features

- 📷 Invoice image upload
- 🔎 OCR-based text extraction using Tesseract
- 🧾 Automated bill field extraction
- ✅ Financial validation and consistency checks
- 🤖 ML-based anomaly detection using Isolation Forest
- 💾 SQLite database for analysis history
- ⚡ FastAPI REST API
- 📖 Automatic Swagger API documentation
- 🖥️ Browser-based dashboard
- 🐳 Dockerized application
- 🔒 Upload type and file-size validation

---

## 🧠 How BillAI Works

```text
Invoice Image
     │
     ▼
OpenCV Preprocessing
     │
     ▼
Tesseract OCR
     │
     ▼
Raw OCR Text
     │
     ▼
Field Extraction
     │
     ├── Vendor
     ├── GST Number
     ├── Bill Number
     ├── Bill Date
     ├── Total Amount
     ├── GST
     ├── Discount
     ├── Round-off
     ├── Payable Amount
     ├── Received Amount
     ├── Payment Mode
     └── Item Count
     │
     ▼
Validation Engine
     │
     ▼
Isolation Forest
     │
     ▼
Analysis Result
     │
     ├── Structured Bill Data
     ├── Validation Status
     └── Anomaly Status + Score
     │
     ▼
SQLite Database
````

---

## 🔬 OCR Pipeline

BillAI uses:

* **OpenCV** for image preprocessing
* **Tesseract OCR** for text recognition
* **Python-based extraction logic** for converting OCR output into structured fields

### Supported Image Formats

* JPG / JPEG
* PNG
* WEBP

### Maximum Upload Size

```text
10 MB
```

---

## 📊 Validation Engine

The validation layer performs basic financial consistency checks.

Examples include:

* Required field validation
* Negative amount detection
* Payable amount consistency
* Discount and round-off calculations
* Received amount vs payable amount comparison

For example, BillAI can check whether:

```text
Total Amount
- Discount
+ Round Off
≈ Payable Amount
```

It also checks an alternative calculation when GST is represented separately.

Validation results are returned as:

```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

---

## 🤖 Anomaly Detection

BillAI includes a prototype anomaly-detection component based on **Isolation Forest**.

The model uses financial and invoice-level features such as:

* Total amount
* GST amount
* Discount
* Payable amount
* Received amount
* Item count

The model produces:

```text
status
anomaly_score
```

Example:

```json
{
  "status": "normal",
  "anomaly_score": 0.1241
}
```

> **Note:** The current anomaly-detection model is trained on synthetic invoice data and is intended as a prototype. It should not be interpreted as a production fraud-detection system.

---

## 🏗️ Project Structure

```text
BillAI/
│
├── app/
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── __init__.py
│   │
│   ├── ml/
│   │   ├── anomaly_model.pkl
│   │   ├── generate_dataset.py
│   │   └── train_anomaly_model.py
│   │
│   ├── models/
│   │   ├── schemas.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── anomaly.py
│   │   ├── extraction.py
│   │   ├── ocr.py
│   │   ├── pipeline.py
│   │   └── validation.py
│   │
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── sample_data/
│   └── invoices.csv
│
├── tests/
│   └── test_ocr.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### OCR & Computer Vision

* Tesseract OCR
* pytesseract
* OpenCV
* Pillow

### Machine Learning

* scikit-learn
* Isolation Forest
* pandas
* NumPy
* joblib

### Database

* SQLite
* SQLAlchemy

### Frontend

* HTML
* CSS
* JavaScript

### Deployment

* Docker
* Uvicorn

---

## 🔌 API

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy",
  "service": "BillAI"
}
```

### Analyze Invoice

```http
POST /analyze
```

Accepts a bill/invoice image and returns:

* Extracted bill data
* Validation results
* Anomaly detection result

### Analysis History

```http
GET /results/{analysis_id}
```

Returns a previously stored analysis.

### API Documentation

When running locally, FastAPI provides interactive Swagger documentation at:

```text
http://localhost:8000/docs
```

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/DevenBedekar07/BillAI.git
cd BillAI
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

BillAI requires Tesseract OCR to process invoice images.

Make sure the Tesseract executable is available on your system PATH.

### 5. Start the application

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

## 🐳 Run with Docker

Build the image:

```bash
docker build -t billai .
```

Run the container:

```bash
docker run -p 8000:8000 billai
```

Then open:

```text
http://localhost:8000
```

---

## 🔐 Data & Security Considerations

BillAI currently:

* Validates uploaded file types
* Limits uploads to 10 MB
* Uses temporary files during processing
* Removes temporary uploaded files after analysis
* Does not expose raw OCR text through the public analysis response
* Does not store uploaded invoice images in the database
* Stores structured analysis results in SQLite

For public demonstrations, synthetic or anonymized invoices should be used.

---

## 📌 Current Limitations

The current version is a prototype and has several areas for future improvement:

* OCR accuracy can vary depending on invoice quality and layout
* Field extraction currently uses rule-based patterns
* Anomaly detection is trained on synthetic data
* No production-grade authentication yet
* No real-world fraud-labelled dataset
* No PDF processing in the current version
* Benchmarking across vendors is not yet implemented

---

## 🔮 Future Improvements

Potential extensions include:

* Layout-aware document understanding
* Better invoice field extraction using transformer-based models
* PDF invoice support
* Vendor benchmarking
* Historical spending analytics
* Duplicate invoice detection
* More sophisticated anomaly detection
* Human-in-the-loop verification
* Role-based authentication
* Cloud database
* Production monitoring
* Model retraining pipelines

---

## 👨‍💻 Author

**Deven Arun Bedekar**

B.Sc. Artificial Intelligence & Machine Learning

GitHub:

[https://github.com/DevenBedekar07](https://github.com/DevenBedekar07)

---

## 📄 License

This project is currently intended as a portfolio and educational project.

````

After pasting:

```powershell
git status
````

You should see only:

```text
modified: README.md
```

