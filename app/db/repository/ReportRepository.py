from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_session

from fastapi import Depends
from app.models.report import Report

class ReportRepository:
  db : AsyncSession
  def __init__(
      self, 
      db: AsyncSession=Depends(get_session)) -> None:
    self.db = db

  async def create_report(self):
    async with self.db as session:
      report = Report()
      session.add(report)
      await session.commit()
      await session.refresh(report)
      return report.id
    
  async def get_report_by_id(self, report_id) -> Report:
    async with self.db as session:
      report = await session.get(Report, report_id)
      if report is None:
        raise Exception(f"Report not found with id: {report_id}")
      return report
  