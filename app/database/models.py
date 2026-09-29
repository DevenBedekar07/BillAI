from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.database.database import Base


class BillAnalysis(Base):
    __tablename__ = "bill_analyses"

    id = Column(Integer, primary_key=True, index=True)

    vendor_name = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)
    bill_number = Column(String, nullable=True)
    bill_date = Column(String, nullable=True)

    total_amount = Column(Float, nullable=True)
    gst_amount = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    round_off = Column(Float, nullable=True)
    payable_amount = Column(Float, nullable=True)
    received_amount = Column(Float, nullable=True)

    payment_mode = Column(String, nullable=True)
    item_count = Column(Integer, nullable=True)

    validation_status = Column(String, nullable=True)
    anomaly_status = Column(String, nullable=True)
    anomaly_score = Column(Float, nullable=True)

    raw_text = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )