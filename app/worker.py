from celery import Celery
from app.utils.config import get_settings
import uuid
from app.db.postgres import get_session
from app.db.repository.ReportRepository import ReportRepository
import asyncio
from app.db.repository.StoreStatusRepository import StoreStatusRepository
from app.db.repository.StoreBusinessHoursRepository import StoreBusinessHoursRepository
from app.db.repository.StoreTimezoneRepository import StoreTimezoneRepository
import pandas as pd
from dateutil import parser
from app.utils.time import get_day_of_week
import pytz
from datetime import timedelta
from app.utils.minio import upload_file_to_minio

# import time
from app.models.report import ReportStatus

settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
)
# MOCK TIME NOW FROM DATASET FOR TESTING
TIME_NOW = "2023-01-25 18:13:22.47922 UTC"
# parsing TIME_NOW to datetime
TIME_NOW = parser.parse(TIME_NOW)


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


@celery_app.task(name="generate_report")
def generate_report(report_id: uuid.UUID):
    """
    generate_report is a celery task which is used to generate the report
    it is called by the create_report endpoint
    """

    async def generate_report_and_update_status():
        """
        update_report_url_and_status is an async function which is used to update the report url and status


        """
        async with get_session() as session:
            store_status_repository = StoreStatusRepository(session)
            store_ids = await store_status_repository.get_store_ids()
            master_data = []
            for store_id in store_ids[:10]:
                store_timezone_repository = StoreTimezoneRepository(session)
                store_timezone = await store_timezone_repository.get_store_timezone(
                    store_id
                )
                store_business_hours_repository = StoreBusinessHoursRepository(session)
                df_store_business_hours = await store_business_hours_repository.get_store_business_hours_in_df(
                    store_id
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
                df_store_status = df_store_status[
                    df_store_status["is_business_hr"] == True
                ]

                # convert TIME_NOW to local timezone
                TIME_NOW_LOCAL = TIME_NOW.astimezone(pytz.timezone(store_timezone))
                time_limits = calculate_times(TIME_NOW_LOCAL)

                uptime_report = list(
                    map(
                        lambda x: df_store_status[
                            df_store_status["timestamp_local"] > x
                        ]["uptime"].sum(),
                        time_limits,
                    )
                )

                downtime_report = list(
                    map(
                        lambda x: df_store_status[
                            df_store_status["timestamp_local"] > x
                        ]["downtime"].sum(),
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

            # pd.DataFrame(master_data).to_csv("report.csv", index=False)
            csv_data = pd.DataFrame(master_data).to_csv(index=False)
            encoded_data = csv_data.encode("utf-8")
            repo = ReportRepository(session)

            blob_object_name = f"{report_id}.csv"
            uploaded_url = settings.MINIO_DOWNLOAD_ENDPOINT + blob_object_name

            # Upload the file to minio
            upload_file_to_minio(blob_object_name, encoded_data, "application/csv")

            response = await repo.update_report_url(report_id, uploaded_url)

            if response.status != ReportStatus.COMPLETED:
                raise Exception("Unable to update report url")
            else:
                print("Report url updated successfully")

            session.close()

    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(generate_report_and_update_status())
    except Exception as e:
        print(str(e))
        raise Exception("Unable to update report url")


celery_app.register_task(generate_report)
