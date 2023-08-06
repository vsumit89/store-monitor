from app.db.repository.ReportRepository import ReportRepository
from fastapi import Depends
from app.models.report import Report

class ReportService:
  report_repository : ReportRepository 
  def __init__(
      self,
      reportRepository: ReportRepository = Depends()
    ) -> None:
    self.report_repository = reportRepository
    

  def create_report(self):
    return self.report_repository.create_report()
  
  def get_report_by_id(self, report_id) -> Report:
    return self.report_repository.get_report_by_id(report_id)