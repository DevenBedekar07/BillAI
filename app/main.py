from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

import shutil
import tempfile
import os

from app.services.pipeline import analyze_bill
from app.models.schemas import AnalysisResponse

from app.database.database import Base, engine, get_db
from app.database import models
from app.database.models import BillAnalysis
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="BillAI",
    description="AI-powered invoice and bill analysis API",
    version="1.0.0"
)
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse("frontend/index.html")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "BillAI"
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check that a file was uploaded
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided."
        )

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload JPG, PNG, or WEBP."
        )

    # Create a temporary file
    suffix = os.path.splitext(file.filename)[1]
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    temp_path = None

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum allowed size is 10 MB."
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:
        temp_file.write(file_content)
        temp_path = temp_file.name

    try:
        # Run the complete BillAI pipeline
        result = analyze_bill(temp_path)

        bill_data = result["bill_data"]
        validation = result["validation"]
        anomaly = result["anomaly"]

        # Create database record
        db_record = BillAnalysis(
            vendor_name=bill_data.get("vendor_name"),
            gst_number=bill_data.get("gst_number"),
            bill_number=bill_data.get("bill_number"),
            bill_date=bill_data.get("bill_date"),

            total_amount=bill_data.get("total_amount"),
            gst_amount=bill_data.get("gst_amount"),
            discount=bill_data.get("discount"),
            round_off=bill_data.get("round_off"),
            payable_amount=bill_data.get("payable_amount"),
            received_amount=bill_data.get("received_amount"),

            payment_mode=bill_data.get("payment_mode"),
            item_count=bill_data.get("item_count"),

            validation_status=(
                "valid"
                if validation.get("valid")
                else "invalid"
            ),

            anomaly_status=anomaly.get("status"),
            anomaly_score=anomaly.get("anomaly_score"),

            
        )

        # Save analysis to SQLite
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return result

    except Exception as e:

        # Roll back database transaction if something fails
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Bill analysis failed: {str(e)}"
        )

    finally:

        # Delete temporary uploaded file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
@app.get("/results/{analysis_id}")
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    record = (
        db.query(BillAnalysis)
        .filter(BillAnalysis.id == analysis_id)
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return {
        "id": record.id,
        "bill_data": {
            "vendor_name": record.vendor_name,
            "gst_number": record.gst_number,
            "bill_number": record.bill_number,
            "bill_date": record.bill_date,
            "total_amount": record.total_amount,
            "gst_amount": record.gst_amount,
            "discount": record.discount,
            "round_off": record.round_off,
            "payable_amount": record.payable_amount,
            "received_amount": record.received_amount,
            "payment_mode": record.payment_mode,
            "item_count": record.item_count
        },
        "validation": {
            "status": record.validation_status
        },
        "anomaly": {
            "status": record.anomaly_status,
            "score": record.anomaly_score
        },
        "created_at": record.created_at
    }