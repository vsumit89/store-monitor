from fastapi import APIRouter
from fastapi import Depends, Response
from app.schema.report import CreateReportResponse, GetReportResponse, GetReportRequestSchema
from app.service.report import ReportService

""" 
report_router is the router which will be used to define 
 - trigger report endpoint  - /trigger_report
 - get report endpoint      - /get_report
"""
report_router = APIRouter()

@report_router.get("/trigger_report", response_model=CreateReportResponse)
async def trigger_report(response: Response, report_service: ReportService = Depends()):
    try:
      reportID = await report_service.create_report()
      responseBody = CreateReportResponse(
      message="report created successfully",
      report_id=reportID
      )
    except Exception as e:
      print(str(e))
      responseBody = CreateReportResponse(
      message="Unable to create report. Please try again later.",
      report_id=None
      )
      response.status_code = 500

    return responseBody


@report_router.post("/get_report")
async def get_report(response: Response, requestBody: GetReportRequestSchema, report_service: ReportService = Depends()):
    try:
      report = await report_service.get_report_by_id(requestBody.report_id)
      responseBody = GetReportResponse(
        message="successfully retrieved report",
        report=report
      )
    except Exception as e:
      print(str(e))
      response.status_code = 500
      responseBody = GetReportResponse(
        message=str(e),
        report=None
      )

    return responseBody.dict(exclude_none=True)


# @report_router.post("/update_report")
# async def update_report(response: Response, requestBody: GetReportRequestSchema, report_service: ReportService = Depends()):
#     try:
#       report = await report_service.update_report(requestBody.report_id, "https://www.google.com")
#       responseBody = GetReportResponse(
#         message="successfully updated report",
#         report=report
#       )
#     except Exception as e:
#       print(str(e))
#       response.status_code = 500
#       responseBody = GetReportResponse(
#         message=str(e),
#         report=None
#       )

#     return responseBody.dict(exclude_none=True)