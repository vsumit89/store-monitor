from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_session
from sqlmodel import select
from fastapi import Depends
from app.models.store_status import StoreStatus
from dateutil import parser
import pandas as pd


class StoreStatusRepository:
    """
    StoreStatusRepository handles database operations related to StoreStatus model.
    """

    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        """
        Constructor for StoreStatusRepository class.

        Parameters:
        - db (AsyncSession): An instance of AsyncSession for database interactions.
        """
        self.db = db

    async def get_store_status_in_df(self, store_id) -> pd.DataFrame:
        """
        Retrieves store status data for a given store ID and returns the data in a DataFrame.

        Parameters:
        - store_id (int): The ID of the store.

        Returns:
        - pd.DataFrame: DataFrame containing store status data.
        """
        async with self.db as session:
            statement = (
                select(
                    StoreStatus.store_id, StoreStatus.status, StoreStatus.timestamp_utc
                )
                .where(StoreStatus.store_id == store_id)
                .order_by(StoreStatus.timestamp_utc)
            )
            result = await session.execute(statement)
            result = result.fetchall()

            # create a dataframe from the result
            column_names = ["store_id", "status", "timestamp_utc"]
            store_statuses = pd.DataFrame(result, columns=column_names)
            return store_statuses

    async def get_store_ids(self):
        """
        Retrieves distinct store IDs from the database.

        Returns:
        - list: A list of distinct store IDs.
        """
        async with self.db as session:
            statement = select(StoreStatus.store_id).distinct()
            result = await session.execute(statement)
            store_ids = []
            # use lambda function to get store_id from result
            store_ids = list(map(lambda x: x, result.scalars()))
            return store_ids
