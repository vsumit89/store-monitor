from sqlmodel import Field, SQLModel, Column
from sqlalchemy import BigInteger
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
    __tablename__ = "store_status"

    id: int = Field(default=None, primary_key=True)
    store_id: int = Field(default=None, sa_column=Column(BigInteger()))
    status: Status
    timestamp_utc: str 
