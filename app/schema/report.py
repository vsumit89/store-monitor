from pydantic import BaseModel
import uuid
from app.models.report import Report



class CreateReportResponse(BaseModel):
    """
    CreateReportResponse Schema is used to define the response body of the create report endpoint
    Attributes:
        message - string representing the message of the response
        report_id - uuid.UUID representing the id of the report
    """
    message: str 
    report_id: uuid.UUID | None

class GetReportResponse(BaseModel):
    """
    GetReportResponse Schema is used to define the response body of the get report endpoint
    Attributes:
        message - string representing the message of the response
        report - Report record corresponing to the report_id which is passed in the request body
    """
    message: str 
    report: Report | None
    

    
class GetReportRequestSchema(BaseModel):
    """
    GetReportRequestSchema Schema is used to define the request body of the get report endpoint
    Attributes:
        report_id - uuid.UUID representing the id of the report
    """
    report_id: uuid.UUID


