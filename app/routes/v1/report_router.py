from fastapi import APIRouter
from fastapi import Depends, Response
from app.schema.report import (
    CreateReportResponse,
    GetReportResponse,
    GetReportRequestSchema,
)
from app.service.report import ReportService

# Define the report_router for report-related endpoints
report_router = APIRouter()


@report_router.get("/trigger_report", response_model=CreateReportResponse)
async def trigger_report(response: Response, report_service: ReportService = Depends()):
    """
    Trigger the creation of a new report.

    Parameters:
        response (Response): FastAPI Response object.
        report_service (ReportService): Dependency to the ReportService.

    Returns:
        CreateReportResponse: Response with the status of the report creation.
    """
    try:
        reportID = await report_service.create_report()
        responseBody = CreateReportResponse(
            message="report created successfully", report_id=reportID
        )
    except Exception as e:
        print(str(e))
        responseBody = CreateReportResponse(
            message="Unable to create report. Please try again later.", report_id=None
        )
        response.status_code = 500

    return responseBody


@report_router.post("/get_report", response_model=GetReportResponse)
async def get_report(
    response: Response,
    requestBody: GetReportRequestSchema,
    report_service: ReportService = Depends(),
):
    """
    Get a report by its ID.

    Parameters:
        response (Response): FastAPI Response object.
        request_body (GetReportRequestSchema): Request body containing the report ID.
        report_service (ReportService): Dependency to the ReportService.

    Returns:
        dict: Dictionary containing the retrieved report information.
    """
    try:
        report = await report_service.get_report_by_id(requestBody.report_id)
        responseBody = GetReportResponse(
            message="successfully retrieved report", report=report
        )
    except Exception as e:
        response.status_code = 500
        responseBody = GetReportResponse(message=str(e), report=None)

    return responseBody
