from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_session

from fastapi import Depends
from app.models.report import Report, ReportStatus


class ReportRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        """
        Constructor for ReportRepository class.

        Parameters:
        - db (AsyncSession): An instance of the AsyncSession for database interactions.
        """
        self.db = db

    async def create_report(self):
        """
        Creates a new report record in the database and returns the report id.
        Returns:
        - int: The ID of the newly created report.
        """
        async with self.db as session:
            report = Report()
            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report.id

    async def get_report_by_id(self, report_id) -> Report:
        """
        Retrieves a report from the database by its ID.

        Parameters:
        - report_id (int): The ID of the report to retrieve.

        Returns:
        - Report: The retrieved Report object.

        Raises:
        - Exception: If no report is found with the specified ID.
        """
        async with self.db as session:
            report = await session.get(Report, report_id)
            if report is None:
                raise Exception(f"Report not found with id: {report_id}")
            return report

    async def update_report_url(self, report_id, url) -> Report:
        """
        Updates the URL and status of a report in the database.

        Parameters:
        - report_id (int): The ID of the report to update.
        - url (str): The new URL for the report.

        Returns:
        - Report: The updated Report object.

        Raises:
        - Exception: If no report is found with the specified ID.
        """
        async with self.db as session:
            report = await session.get(Report, report_id)
            if report is None:
                raise Exception(f"Report not found with id: {report_id}")
            report.url = url
            report.status = ReportStatus.COMPLETED

            await session.commit()
            await session.refresh(report)
            return report
