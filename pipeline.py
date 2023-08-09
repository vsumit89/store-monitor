from sqlalchemy import create_engine
import pandas as pd
import logging
import asyncio
from contextlib import asynccontextmanager
import uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import get_settings

settings = get_settings()
# Create an asynchronous engine for the database
engine = create_async_engine(
    f"postgresql+asyncpg://postgres:postgres@localhost:5432/store_monitor",
    echo=True,
    future=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE,
)


# Asynchronous context manager for creating database sessions
@asynccontextmanager
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def load_data_from_csv_and_store(filename):

    # load the data from the csv file
    logging.info("Loading data from csv file - " + filename + ".csv")
    df = pd.read_csv("./datastore/" + filename + ".csv")
    logging.info("Data loaded from csv file" + filename + ".csv")
    # create the engine to connect to the database - postgres
    logging.info("Creating engine to connect to the database")
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/store_monitor"
    )
    logging.info("Engine created to connect to the database")
    # write the data to the database
    logging.info("Writing data to the database from " + filename + ".csv")

    df.to_sql(filename, engine, index=False, if_exists="replace")
    logging.info("Data written to the database from " + filename + ".csv")


fileName = ["store_business_hours", "store_status", "store_timezone"]

# def getSchemaFromFileName(fileName):
#     if fileName == "store_business_hours":
#         return {
#             "id": "INT",
#             "store_id": "INT",
#             "day": "INT",
#             "start_time_local": "TIME",
#             "end_time_local": "TIME"
#         }
    
#     elif fileName == "store_status":
#         return {
#             "id": "INT",
#             "store_id": "INT",
#             "status": "INT",
#             "timestamp_utc": "TIME",
#             "": "TIME"
#         }
#     elif fileName == "store_timezone":
#         return "store_timezone"
#     else:
#         return "store_status"
async def load_data_from_csv_and_ingest(file):
    logging.info("Loading data from csv file - " + file + ".csv")
    df = pd.read_csv("./datastore/" + file + ".csv", chunksize=1000)

    async with get_session() as session:
        async with session.begin():
            for chunk in df:        
                await session.execute(
                    "INSERT INTO "
                    + file
                    + " VALUES "
                    + str(tuple(chunk.values))
                    + ";"
                )


async def main():
    file_names = ["store_business_hours", "store_status", "store_timezone"]
    tasks = [load_data_from_csv_and_store(file_name) for file_name in file_names]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
