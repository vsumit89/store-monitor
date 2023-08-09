from app.db.repository.ReportRepository import ReportRepository
from fastapi import Depends
from app.models.report import Report
from app.worker import generate_report


class ReportService:
    """
    ReportService class contains the business logic for report-related endpoints.
    It interacts with the ReportRepository class to perform database operations.
    """

    report_repository: ReportRepository

    def __init__(self, reportRepository: ReportRepository = Depends()) -> None:
        """
        Constructor for ReportService class.

        Parameters:
        - report_repository (ReportRepository): An instance of the ReportRepository class
          used for interacting with the database.

        Initializes the ReportService with the specified ReportRepository.
        """
        self.report_repository = reportRepository

    async def create_report(self):
        """
        create_report method creates a report record in the database and triggers
        the generate_report Celery task.
        """
        try:
            reportid = await self.report_repository.create_report()
            generate_report.apply_async(
                args=[
                    reportid,
                ]
            )
        except Exception as e:
            print(str(e))
            raise Exception("Unable to create report. Please try again later.")

        return reportid

    def get_report_by_id(self, report_id) -> Report:
        """
        Retrieves a report from the database by its ID.
        """
        return self.report_repository.get_report_by_id(report_id)

    def update_report(self, report_id, url) -> Report:
        """
        Updates the URL of a report in the database.
        """
        return self.report_repository.update_report_url(report_id, url)
