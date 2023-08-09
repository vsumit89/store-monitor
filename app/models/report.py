from sqlmodel import SQLModel, Field
import uuid
from enum import Enum


class ReportStatus(str, Enum):
    """
    Enum representing the status of a report.

    Attributes:
        RUNNING (str): Represents the report is running.
        COMPLETED (str): Represents the report is completed.
    """

    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"


class Report(SQLModel, table=True):
    """
    Model representing a report for all the stores.

    Attributes:
        id (uuid.UUID): The ID of the report.
        status (ReportStatus): The status of the report.
        url (str, optional): The URL of the report.
    """

    __tablename__ = "reports"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: ReportStatus = Field(default=ReportStatus.RUNNING)
    url: str | None = Field(default=None)
