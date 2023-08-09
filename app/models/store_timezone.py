from sqlalchemy import Column, BigInteger
from sqlmodel import Field, SQLModel


class StoreTimezone(SQLModel, table=True):
    """
    Model representing the timezone of a store.

    Attributes:
        store_id (int): The ID of the store.
        timezone_str (str): The timezone of the store.
    """

    __tablename__ = "store_timezone"
    id: int = Field(default=None, primary_key=True)
    store_id: int = Field(sa_column=Column(BigInteger()))
    timezone_str: str = Field(default=None, nullable=False)
