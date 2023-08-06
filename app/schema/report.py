from pydantic import BaseModel
import uuid
from app.models.report import Report

class CreateReportResponse(BaseModel):
    message: str 
    report_id: uuid.UUID | None

class GetReportResponse(BaseModel):
    message: str 
    report: Report | None
    

    
class GetReportRequestSchema(BaseModel):
    report_id: uuid.UUID


