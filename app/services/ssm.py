import logging
from collections.abc import Iterable

import boto3

logger = logging.getLogger(__name__)


def get_ssm_parameters(
    ssm_names: Iterable,
    ssm_name_prefix: str,
    region_name: str,
) -> Iterable:
    """AWS Systems Manager からパラメータを取得
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters.html
    """
    ssm = boto3.client("ssm", region_name=region_name)

    response = ssm.get_parameters(
        Names=[ssm_name_prefix + param for param in ssm_names],
        WithDecryption=True,
    )
    logger.info(f"Successfully ssm parameters: {response}")
    return response["Parameters"]
