from sqlmodel import SQLModel, Field, Column
from sqlalchemy import BigInteger
from datetime import time

# from .store_timezone import StoreTimezone


class StoreBusinessHours(SQLModel, table=True):
    """
    StoreBusinessHours model represents the business hours of a store
    Attributes:
      store_id - big integer representing the id of the store
      day - integer representing the day of the week
      open_time - datetime representing the time the store opens
      close_time - datetime representing the time the store closes
    """
    def __init__(self, store_id, day, start_time_local, end_time_local):
        self.store_id = store_id
        self.day = day
        self.start_time_local = start_time_local
        self.end_time_local = end_time_local
        
    __tablename__ = "store_business_hours"
    id: int = Field(default=None, primary_key=True)
    store_id: int = Field(sa_column=Column(BigInteger()))
    day: int
    start_time_local: str
    end_time_local: str
