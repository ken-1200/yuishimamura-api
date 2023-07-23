import logging

from botocore.exceptions import BotoCoreError, ClientError

from app.boto3_client import init_client
from app.date_utils import make_time_ns
from app.settings import Settings

settings = Settings()

logger = logging.getLogger(__name__)


def create_invalidation() -> None:
    """https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/client/create_invalidation.html#CloudFront.Client.create_invalidation"""
    cloudfront = init_client("cloudfront")

    try:
        invalidation = cloudfront.create_invalidation(
            DistributionId=settings.DISTRIBUTION_ID,
            InvalidationBatch={
                "Paths": {"Quantity": 1, "Items": ["/*"]},
                "CallerReference": str(make_time_ns()),
            },
        )
        logger.info(f"Created invalidation: {invalidation}")
    except (BotoCoreError, ClientError) as error:
        logger.error(error)
        raise error
