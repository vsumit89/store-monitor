from pydantic import BaseModel
import uuid
from app.models.report import Report


class CreateReportResponse(BaseModel):
    """
    Schema for the response body of the create report endpoint.

    Attributes:
        message (str): A string representing the message of the response.
        report_id (uuid.UUID): The ID of the newly created report. Can be None.
    """

    message: str
    report_id: uuid.UUID | None


class GetReportResponse(BaseModel):
    """
    Schema for the response body of the get report endpoint.

    Attributes:
        message (str): A string representing the message of the response.
        report (Report): A Report object corresponding to the report_id in the request.
    """

    message: str
    report: Report | None


class GetReportRequestSchema(BaseModel):
    """
    Schema for the request body of the get report endpoint.

    Attributes:
        report_id (uuid.UUID): The ID of the report to retrieve.
    """

    report_id: uuid.UUID
