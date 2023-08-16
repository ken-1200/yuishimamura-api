import json
import logging
from collections.abc import Mapping
from typing import Any, Type, TypeVar

from fastapi import BackgroundTasks, Request

from app.async_utils import to_subthread
from app.exceptions.exception import S3DeleteObjectError, YuishimamuraAPIBaseException
from app.services.s3 import delete_object, put_object
from app.settings import Settings

from .schema import UpdateDeleteImageRequest

logger = logging.getLogger(__name__)

settings = Settings()

I = TypeVar("I", bound=YuishimamuraAPIBaseException)


class UpdateDeleteImage:
    def __init__(self, request: Request, background_tasks: BackgroundTasks) -> None:
        self.request = request
        self.background_tasks = background_tasks

    async def execute(self, params: UpdateDeleteImageRequest) -> Mapping[str, Any]:
        logger.info("UpdateDeleteImage", extra=params.model_dump())

        # S3の画像を削除
        try:
            s3_uris = [
                await to_subthread(
                    delete_object,
                    settings.BUCKET_NAME,
                    object_path.replace("/", "", 1),
                )
                for object_path in params.images_path
            ]

        except Exception as error:
            logger.error(f"Failed to delete images to S3.: {error}", exc_info=True)
            raise await self.convert_error(repr(error), S3DeleteObjectError)

        # 削除対象以外の要素
        params.images_json["images"] = [
            image_json
            for image_json in params.images_json["images"]
            if image_json["src"] not in params.images_path
        ]

        # S3にJSONファイルをアップロード
        try:
            images_json_bytes = json.dumps(params.images_json).encode("utf-8")
            object_path = "images.json"
            await to_subthread(
                put_object,
                images_json_bytes,
                settings.BUCKET_NAME,
                object_path,
            )

        except Exception as error:
            logger.error(
                f"Failed to upload binary json data to S3.: {error}", exc_info=True
            )
            raise await self.convert_error(repr(error), S3DeleteObjectError)

        return {"status_code": 200, "s3_uris": s3_uris}

    async def convert_error(
        self,
        error: str,
        exc_class: Type[I],
    ) -> YuishimamuraAPIBaseException:
        return exc_class(body={"message": error})
