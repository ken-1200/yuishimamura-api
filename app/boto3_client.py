import boto3

from app.common import cache
from app.settings import Settings

settings = Settings()


@cache(seconds=300)
def init_client(service_name: str):
    if settings.env == "local":
        session = boto3.session.Session(profile_name=settings.PROFILE_NAME)
        return session.client(service_name)
    else:
        return boto3.client(service_name, region_name=settings.REGION_NAME)
