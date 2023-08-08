from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import get_settings
from sqlmodel import select
from app.models.store_status import StoreStatus
from app.models.store_business_hours import StoreBusinessHours
from app.models.store_timezone import StoreTimezone
from app.db.repository.StoreStatusRepository import StoreStatusRepository
from app.db.repository.StoreBusinessHoursRepository import StoreBusinessHoursRepository
from app.db.repository.StoreTimezoneRepository import StoreTimezoneRepository
import pytz
import pandas as pd
# from datetime import datetime, timedelta


settings = get_settings()
# Create an asynchronous engine for the database
engine = create_async_engine(
    f"postgresql+asyncpg://postgres:postgres@localhost:5432/store_monitor",
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_recycle=20,
)


# Asynchronous context manager for creating database sessions
@asynccontextmanager
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

# Define a function to convert local time to UTC and handle day change
def local_to_utc_with_day(store_timezone, local_time, local_day):
    timezone_obj = pytz.timezone(store_timezone)
    local_time = timezone_obj.localize(local_time)
    utc_time = local_time.astimezone(pytz.UTC)
    
    # Check if the day has changed due to timezone shift
    if utc_time.date() != local_time.date():
        local_day += 1
    
    return utc_time, local_day



async def generate_report():
    async with get_session() as session:
        query = select(StoreStatus.store_id).distinct()
        result = await session.execute(query)
        store_ids = []
        # use lambda function to get store_id from result
        store_ids = list(map(lambda x: x, result.scalars()))
    
        for store_id in store_ids[1:2]:
            store_timezone_repository = StoreTimezoneRepository(session)
            store_timezone = await store_timezone_repository.get_store_timezone(8139926242460185114)
            store_business_hours_repository = StoreBusinessHoursRepository(session)
            df_store_business_hours = await store_business_hours_repository.get_store_business_hours_in_df(store_id)
            print(df_store_business_hours)
            df_store_business_hours["start_time_local"] = pd.to_datetime(df_store_business_hours["start_time_local"])
            df_store_business_hours["end_time_local"] = pd.to_datetime(df_store_business_hours["end_time_local"])
            df_store_business_hours['start_time_utc'], df_store_business_hours['day'] = zip(*df_store_business_hours.apply(lambda row: local_to_utc_with_day(store_timezone, row['start_time_local'], row['day']), axis=1))
            df_store_business_hours['end_time_utc'], _ = zip(*df_store_business_hours.apply(lambda row: local_to_utc_with_day(store_timezone, row['end_time_local'], row['day']), axis=1))      
            print(df_store_business_hours)

            

        # Close the session
        session.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(generate_report())
