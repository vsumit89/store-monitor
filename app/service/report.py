from app.db.repository.ReportRepository import ReportRepository
from fastapi import Depends
from app.models.report import Report
from app.worker import generate_report


class ReportService:
  """
    ReportService class is used to define the business logic of the report endpoints
    it is used to interact with the ReportRepository class
  """
  report_repository : ReportRepository 
  def __init__(
      self,
      reportRepository: ReportRepository = Depends()
    ) -> None:
    self.report_repository = reportRepository
    

  async def create_report(self):
    """
    create_report method creates the report record into the database
    it also calls the generate_report celery task
    """
    try:
      reportid = await self.report_repository.create_report()
      generate_report.apply_async(args=[reportid,])
    except Exception as e:
      print(str(e))
      raise Exception("Unable to create report. Please try again later.")
    
    return reportid
  
  
  def get_report_by_id(self, report_id) -> Report:
    return self.report_repository.get_report_by_id(report_id)
  
  def update_report(self, report_id, url) -> Report:
    return self.report_repository.update_report_url(report_id, url)