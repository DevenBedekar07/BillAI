from typing import Optional
from pydantic import BaseModel


class BillData(BaseModel):
    vendor_name: Optional[str] = None
    gst_number: Optional[str] = None
    bill_number: Optional[str] = None
    bill_date: Optional[str] = None
    total_amount: Optional[float] = None
    gst_amount: Optional[float] = None
    discount: Optional[float] = None
    round_off: Optional[float] = None
    payable_amount: Optional[float] = None
    received_amount: Optional[float] = None
    payment_mode: Optional[str] = None
    item_count: Optional[int] = None
class ValidationResult(BaseModel):
    valid: bool
    errors: list[str]
    warnings: list[str]


class AnomalyResult(BaseModel):
    status: str
    anomaly_score: float


class AnalysisResponse(BaseModel):
    bill_data: BillData
    validation: ValidationResult
    anomaly: AnomalyResult
  