from sqlalchemy import Column, BigInteger
from sqlmodel import Field, SQLModel


class StoreTimezone(SQLModel, table=True):
  """
    StoreTimezone model represents the timezone of a store
    Attributes:
      store_id - big integer representing the id of the store
      timezone - string representing the timezone of the store
  """
  __tablename__ = "store_timezone"
  id: int = Field(default=None, primary_key=True)
  store_id: int = Field(sa_column=Column(BigInteger()))
  timezone_str: str = Field(default=None, nullable=False)