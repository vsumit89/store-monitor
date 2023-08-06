from sqlmodel import SQLModel
from datetime import datetime


class StoreBusinessHours(SQLModel, table=True):
  """
    StoreBusinessHours model represents the business hours of a store
    Attributes:
      store_id - big integer representing the id of the store
      day - integer representing the day of the week
      open_time - datetime representing the time the store opens
      close_time - datetime representing the time the store closes
  """
  __tablename__ = "store_business_hours"
  store_id: int 
  day: int 
  start_time_local: datetime 
  end_time_local: datetime 