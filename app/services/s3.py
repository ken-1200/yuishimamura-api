import base64
import io
import logging
import re
import time

from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image

from app.boto3_client import init_client

logger = logging.getLogger(__name__)


def make_time_ns() -> int:
    """ナノ秒のタイムスタンプを生成"""
    return time.time_ns()


def convert_b64_string_to_bynary(string: str) -> bytes:
    """デコードする"""
    return base64.b64decode(string.encode("UTF-8"))


def process_base64_image(base64_data: bytes) -> tuple[str, bytes] | tuple[None, None]:
    # 画像形式の正規表現パターン
    image_pattern = re.compile(rb"data:image/(.*?);base64,")

    # 画像形式のマッチング
    image_match = image_pattern.match(base64_data)

    if image_match:
        # マッチした画像形式
        image_type = image_match.group(1).decode("utf-8")

        # 画像形式に応じて識別子を置換
        base64_data = re.sub(rb"data:image/.*?;base64,", b"", base64_data)

        # Base64データをバイナリ形式に変換
        binary_data = base64.b64decode(base64_data)

        return image_type, binary_data

    return None, None


def convert_to_webp(binary_data: bytes) -> bytes:
    # バイナリデータをPillowのImageオブジェクトに変換
    image = Image.open(io.BytesIO(binary_data))

    # WebP形式に変換
    webp_data = io.BytesIO()
    image.save(webp_data, format="WebP", quality=85)

    # WebPデータをバイナリ形式に変換して返す
    return webp_data.getvalue()


def put_object(binary_data: bytes, bucket_name: str, object_path: str) -> str:
    """バイナリデータをS3にアップロードする

    :param binary_data: バイナリデータ
    :param bucket_name: アップロード先のバケット名
    :param object_path: オブジェクトのパス
    :return アップロード先の URI
    """
    s3 = init_client("s3")

    try:
        s3.put_object(Body=binary_data, Bucket=bucket_name, Key=object_path)
        logger.info(f"Uploaded binary data to: {object_path}")
    except (BotoCoreError, ClientError) as error:
        logger.error(error)
        raise error

    return f"s3://{bucket_name}/{object_path}"


def delete_object(bucket_name: str, object_path: str) -> str:
    """S3のオブジェクトを削除する

    :param bucket_name: アップロード先のバケット名
    :param object_path: オブジェクトのパス
    :return 削除したオブジェクトの URI
    """
    s3 = init_client("s3")

    try:
        s3.delete_object(Bucket=bucket_name, Key=object_path)
        logger.info(f"Deleted object to: {object_path}")
    except (BotoCoreError, ClientError) as error:
        logger.error(error)
        raise error

    return f"s3://{bucket_name}/{object_path}"
