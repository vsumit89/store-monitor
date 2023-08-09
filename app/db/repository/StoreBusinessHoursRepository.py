from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_session
from sqlmodel import select
from fastapi import Depends
from app.models.store_business_hours import StoreBusinessHours
import pandas as pd

class StoreBusinessHoursRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db = db

    async def get_store_business_hours_in_df(self, store_id):
        async with self.db as session:
            statement = select(
                StoreBusinessHours.store_id,
                StoreBusinessHours.day,
                StoreBusinessHours.start_time_local,
                StoreBusinessHours.end_time_local,
            ).where(StoreBusinessHours.store_id == store_id).order_by(StoreBusinessHours.day, StoreBusinessHours.start_time_local)

            result = await session.execute(statement)
            data = result.fetchall()
            column_names = ["store_id", "day", "start_time_local", "end_time_local"]
            if len(data) == 0:
              business_hours = [
                (
                    store_id, day, "00:00:00", "23:59:59"
                )
                for day in range(7)
            ]
              
              return pd.DataFrame(business_hours, columns=column_names)    
            else:
              business_hours_dict_list = [
                  {
                      "store_id": row[0],
                      "day": row[1],
                      "start_time_local": row[2],
                      "end_time_local": row[3],
                  }
                  for row in data
              ]

            return pd.DataFrame(business_hours_dict_list)

