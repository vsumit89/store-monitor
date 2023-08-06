from celery import Celery
from app.utils.config import get_settings
import uuid 
from app.db.postgres import get_session
from app.db.repository.ReportRepository import ReportRepository
import asyncio
import time
from app.models.report import Report

settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
)

@celery_app.task(name="generate_report")
def generate_report(report_id: uuid.UUID):
    """
    generate_report is a celery task which is used to generate the report
    it is called by the create_report endpoint
    """
    async def update():
        async with get_session() as session:
            time.sleep(10)
            repo = ReportRepository(session)
            response = await repo.update_report_url(report_id, 'https://www.google.com')
            if response.status != "COMPLETED":
                raise Exception("Unable to update report url")
            else:
                print("Report url updated successfully")

    try:
        asyncio.run(update())
    except Exception as e:
        print(str(e))
        raise Exception("Unable to update report url")
    



celery_app.register_task(
    generate_report
)


