import json
import logging
from collections.abc import Mapping
from typing import Any, Type, TypeVar

from fastapi import BackgroundTasks, Request

from app.async_utils import to_subthread
from app.date_utils import make_time_ns
from app.exceptions.exception import S3UploadError, YuishimamuraAPIBaseException
from app.services.s3 import convert_to_webp, process_base64_image, put_object
from app.settings import Settings

from .schema import UploadImageRequest

logger = logging.getLogger(__name__)

settings = Settings()

I = TypeVar("I", bound=YuishimamuraAPIBaseException)


class UploadImage:
    def __init__(self, request: Request, background_tasks: BackgroundTasks) -> None:
        self.request = request
        self.background_tasks = background_tasks

    async def execute(self, params: UploadImageRequest) -> Mapping[str, Any]:
        logger.info("UploadImage", extra=params.model_dump())
        s3_uris = []

        # S3に画像をアップロード
        try:
            for image in params.images:
                # data:image/xxx;base64, プレフィックスを除去
                image_type, binary_data = process_base64_image(image)
                logger.info(f"{image_type=} / {binary_data[:10]=}")

                object_path = f"images/IMG_{make_time_ns()}.webp"
                s3_uris.append(
                    await to_subthread(
                        put_object,
                        convert_to_webp(binary_data),
                        settings.BUCKET_NAME,
                        object_path,
                    )
                )

        except Exception as error:
            logger.error(
                f"Failed to upload binary images data to S3.: {error}", exc_info=True
            )
            raise await self.convert_error(repr(error), S3UploadError)

        # リスト内の各要素の id, idx 値を取得して、その中で最大値を見つけます
        _id = max(image["id"] for image in params.images_json["images"])
        _idx = max(image["idx"] for image in params.images_json["images"])

        # S3にJSONファイルをアップロード
        try:
            for s3_uri in s3_uris:
                filename = s3_uri.split("/")[-1]
                _id += 1
                _idx += 1
                params.images_json["images"].append(
                    {
                        "id": _id,
                        "idx": _idx,
                        "src": f"/images/{filename}",
                        "alt": f"{filename}",
                    }
                )
            logger.info(f"images_json: {params.images_json}")

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
            raise await self.convert_error(repr(error), S3UploadError)

        return {"status_code": 200, "s3_uris": s3_uris}

    async def convert_error(
        self,
        error: str,
        exc_class: Type[I],
    ) -> YuishimamuraAPIBaseException:
        return exc_class(body={"message": error})
