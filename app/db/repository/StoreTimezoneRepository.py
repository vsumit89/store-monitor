from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_session
from sqlmodel import select
from fastapi import Depends
from app.models.store_timezone import StoreTimezone


class StoreTimezoneRepository:
    db: AsyncSession

    def __init__(
        self, 
        db: AsyncSession=Depends(get_session)) -> None:
      self.db = db
        

    async def get_store_timezone(self, store_id):
      async with self.db as session:
        statement = select(StoreTimezone.store_id, StoreTimezone.timezone_str).where(StoreTimezone.store_id == store_id)
        result = await session.execute(statement)
        data = result.first()
        if data is None:
          return "America/Chicago"
        else:
          return data[1]

        
        
