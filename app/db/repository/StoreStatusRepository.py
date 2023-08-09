from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_session
from sqlmodel import select
from fastapi import Depends
from app.models.store_status import StoreStatus
from dateutil import parser
import pandas as pd


class StoreStatusRepository:
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db = db

    async def get_store_status_in_df(self, store_id):
        async with self.db as session:
            statement = select(
                StoreStatus.store_id, StoreStatus.status, StoreStatus.timestamp_utc
            ).where(StoreStatus.store_id == store_id).order_by(StoreStatus.timestamp_utc)
            result = await session.execute(statement)
            result = result.fetchall()

            # create a dataframe from the result
            column_names = ["store_id", "status", "timestamp_utc"]
            store_statuses = pd.DataFrame(result, columns=column_names)
            return store_statuses
        

    async def get_store_ids(self):
        async with self.db as session:
            statement = select(StoreStatus.store_id).distinct()
            result = await session.execute(statement)
            store_ids = []
            # use lambda function to get store_id from result
            store_ids = list(map(lambda x: x, result.scalars()))
            return store_ids
