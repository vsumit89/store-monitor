from sqlmodel import SQLModel, Field
import uuid
from enum import Enum

class ReportStatus(str, Enum):
  """
    Status enum represents the status of a store
    Attributes:
      active - string representing the store is active
      inactive - string representing the store is inactive
  """
  RUNNING = "RUNNING"
  COMPLETED = "COMPLETED"

class Report(SQLModel, table=True):
  """
    Report model represents the report of all the stores
    Attributes:
      id - uuid representing the id of the report
      status - string representing the status of the report
      url - string representing the url of the report
  """
  __tablename__ = "reports"
  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  status: ReportStatus = Field(default=ReportStatus.RUNNING)
  url: str | None = Field(default=None)
