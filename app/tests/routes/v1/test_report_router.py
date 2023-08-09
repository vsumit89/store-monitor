import unittest
from fastapi import Response
from unittest.mock import Mock
from fastapi.testclient import TestClient
from app.main import fastapiApp  # Import your FastAPI app instance
from app.service.report import ReportService  # Import your ReportService class
from app.schema.report import CreateReportResponse  # Import your response model

class TestReportRouter(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(fastapiApp)

    def test_trigger_report_success(self):
        # Mock ReportService.create_report to return a report ID
        mock_report_service = Mock(spec=ReportService)
        mock_report_service.create_report.return_value = "report123"
        
        response = self.client.get("/trigger_report")

        self.assertEqual(response.status_code, 200)
        expected_response = CreateReportResponse(
            message="report created successfully",
            report_id="report123"
        )
        self.assertEqual(response.json(), expected_response.dict())

    def test_trigger_report_failure(self):
        # Mock ReportService.create_report to raise an exception
        mock_report_service = Mock(spec=ReportService)
        mock_report_service.create_report.side_effect = Exception("Test error")

        response = self.client.get("/trigger_report")

        self.assertEqual(response.status_code, 500)
        expected_response = CreateReportResponse(
            message="Unable to create report. Please try again later.",
            report_id=None
        )
        self.assertEqual(response.json(), expected_response.dict())

if __name__ == "__main__":
    unittest.main()