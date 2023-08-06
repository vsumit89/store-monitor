from app.models.report import Report
from .postgres import engine


async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(Report.metadata.create_all)


  