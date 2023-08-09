from minio import Minio
from app.utils.config import get_settings
from io import BytesIO
from app.utils.logging import logger

settings = get_settings()
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
)


def upload_file_to_minio(object_name, data, content_type):
    try:
        minio_client.put_object(
            settings.BUCKET_NAME,
            object_name,
            data=BytesIO(data),
            length=len(data),
            content_type=content_type,
        )
        logger.info("Uploaded to minio")
    except Exception:
        raise Exception("Unable to upload to minio")
