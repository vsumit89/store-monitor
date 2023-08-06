from sqlmodel import Field, SQLModel


class StoreTimezone(SQLModel, table=True):
  """
    StoreTimezone model represents the timezone of a store
    Attributes:
      store_id - big integer representing the id of the store
      timezone - string representing the timezone of the store
  """
  store_id: int = Field(default=None, foreign_key="store.id", primary_key=True)
  timezone: str = Field(default=None, nullable=False)