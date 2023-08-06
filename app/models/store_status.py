from sqlmodel import Field, SQLModel
from enum import Enum
from datetime import datetime

class Status(str, Enum):
  """
    Status enum represents the status of a store
    Attributes:
      active - string representing the store is active
      inactive - string representing the store is inactive
  """
  active = "active"
  inactive = "inactive"



class StoreStatus(SQLModel, table=True):
  store_id: int
  status: Status 
  timestamp_utc: datetime