from sqlmodel import SQLModel
from datetime import datetime


class BusinessHours(SQLModel, table=True):
  """
    BusinessHours model represents the business hours of a store
    Attributes:
      store_id - big integer representing the id of the store
      day - integer representing the day of the week
      open_time - datetime representing the time the store opens
      close_time - datetime representing the time the store closes
  """
  __tablename__ = "business_hours"
  store_id: int 
  day: int 
  start_time_local: datetime 
  end_time_local: datetime 