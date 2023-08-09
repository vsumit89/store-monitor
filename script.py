from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import get_settings
from sqlmodel import select
from app.db.repository.StoreStatusRepository import StoreStatusRepository
from app.db.repository.StoreBusinessHoursRepository import StoreBusinessHoursRepository
from app.db.repository.StoreTimezoneRepository import StoreTimezoneRepository
from datetime import datetime, timedelta
import pandas as pd
from dateutil import parser
from app.utils.time import get_day_of_week
import pytz

# from datetime import datetime, timedelta


settings = get_settings()
# MOCK TIME NOW FROM DATASET FOR TESTING
TIME_NOW = "2023-01-25 18:13:22.47922 UTC"
TIME_NOW = parser.parse(TIME_NOW)
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


def get_start_end_time_for_day(dataframe, day):
    day_data = dataframe[dataframe["day"] == day]
    day_data_df = day_data[["start_time_local", "end_time_local"]].values.tolist()
    return day_data_df


def is_timestamp_in_range(timestamp, business_hr_df):
    # to get the index from timestamp
    day_idx = get_day_of_week(timestamp)

    # get the time ranges
    time_ranges = get_start_end_time_for_day(business_hr_df, day_idx)
    return any(
        list(
            map(
                lambda x: pd.to_datetime(x[0], format="%H:%M:%S").time()
                <= timestamp.time()
                <= pd.to_datetime(x[1], format="%H:%M:%S").time(),
                time_ranges,
            )
        )
    )


def calculate_times(time_now):
    # Calculate times
    time_1_hour_ago = time_now - timedelta(hours=1)
    time_1_day_ago = time_now - timedelta(days=1)
    time_1_week_ago = time_now - timedelta(weeks=1)

    return time_1_hour_ago, time_1_day_ago, time_1_week_ago


async def generate_report():
    async with get_session() as session:

        store_status_repository = StoreStatusRepository(session)
        store_ids = await store_status_repository.get_store_ids()

        master_data = []
        for store_id in store_ids[:200]:
            store_timezone_repository = StoreTimezoneRepository(session)
            store_timezone = await store_timezone_repository.get_store_timezone(
                store_id
            )
            store_business_hours_repository = StoreBusinessHoursRepository(session)
            df_store_business_hours = (
                await store_business_hours_repository.get_store_business_hours_in_df(
                    store_id
                )
            )
            # print(df_store_business_hours)
            store_status_repository = StoreStatusRepository(session)
            df_store_status = await store_status_repository.get_store_status_in_df(
                store_id
            )
            df_store_status["timestamp_utc"] = pd.to_datetime(
                df_store_status["timestamp_utc"]
            )
            df_store_status["timestamp_local"] = df_store_status[
                "timestamp_utc"
            ].dt.tz_convert(store_timezone)

            # Calculate time differences
            df_store_status["time_diff"] = df_store_status["timestamp_local"].diff()

            # Calculate downtime
            df_store_status["downtime"] = df_store_status["time_diff"].where(
                df_store_status["status"] == "inactive", pd.NaT
            )

            # Calculate uptime (based on downtime)
            df_store_status["uptime"] = df_store_status["time_diff"].where(
                df_store_status["status"] == "active", pd.NaT
            )

            # Fill missing values with 0 for uptime and downtime
            df_store_status["uptime"] = df_store_status["uptime"].fillna(
                pd.Timedelta(0)
            )
            df_store_status["downtime"] = df_store_status["downtime"].fillna(
                pd.Timedelta(0)
            )

            # add a field to check if the timestamp is in range
            df_store_status["is_business_hr"] = df_store_status[
                "timestamp_local"
            ].apply(lambda x: is_timestamp_in_range(x, df_store_business_hours))
            #  Filter out all the business hours
            df_store_status = df_store_status[df_store_status["is_business_hr"] == True]

            # convert TIME_NOW to local timezone
            TIME_NOW_LOCAL = TIME_NOW.astimezone(pytz.timezone(store_timezone))
            time_limits = calculate_times(TIME_NOW_LOCAL)

            uptime_report = list(
                map(
                    lambda x: df_store_status[df_store_status["timestamp_local"] > x][
                        "uptime"
                    ].sum(),
                    time_limits,
                )
            )


            downtime_report = list(
                map(
                    lambda x: df_store_status[df_store_status["timestamp_local"] > x][
                        "downtime"
                    ].sum(),
                    time_limits,
                )
            )
            report_row = {
                "store_id": store_id,
                "uptime_last_hour": f"{round(uptime_report[0].total_seconds() / 60, 2)} Minutes",
                "uptime_last_day": f"{round(uptime_report[1].total_seconds() / 3600, 2)} Hours",
                "uptime_last_week": f"{round(uptime_report[2].total_seconds() / 3600, 2)} Hours",
                "downtime_last_hour": f"{round(downtime_report[0].total_seconds() / 60, 2)} Minutes",
                "downtime_last_day": f"{round(downtime_report[1].total_seconds() / 3600, 2)} Hours",
                "downtime_last_week": f"{round(downtime_report[2].total_seconds() / 3600, 2)} Hours",
            }
            # print(report_row)
            master_data.append(report_row)

        pd.DataFrame(master_data).to_csv("report.csv", index=False)
        # Close the session
        session.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(generate_report())
