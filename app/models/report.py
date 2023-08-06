from sqlmodel import SQLModel, Field
import uuid

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
  status: str = Field(default="RUNNING")
  url: str | None = Field(default=None)
