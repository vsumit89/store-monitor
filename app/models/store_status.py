from sqlmodel import Field, SQLModel, Column
from sqlalchemy import BigInteger
from enum import Enum
from datetime import datetime


class Status(str, Enum):
    """
    Enum representing the status of a store.

    Attributes:
        active (str): Represents an active store.
        inactive (str): Represents an inactive store.
    """

    active = "active"
    inactive = "inactive"


class StoreStatus(SQLModel, table=True):
    """
    Model representing the status of a store.

    Attributes:
        id (int): The ID of the store status record.
        store_id (int): The ID of the store.
        status (Status): The status of the store.
        timestamp_utc (str): The UTC timestamp when the status was recorded.
    """

    __tablename__ = "store_status"

    id: int = Field(default=None, primary_key=True)
    store_id: int = Field(default=None, sa_column=Column(BigInteger()))
    status: Status
    timestamp_utc: str
