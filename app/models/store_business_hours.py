from sqlmodel import SQLModel, Field, Column
from sqlalchemy import BigInteger
from datetime import time

# from .store_timezone import StoreTimezone


class StoreBusinessHours(SQLModel, table=True):
    """
        Model represents the business hours of a store
        Attributes:
    Attributes:
            store_id (int): The ID of the store.
            day (int): The day of the week.
            start_time_local (str): The time the store opens in local time.
            end_time_local (str): The time the store closes in local time.
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
