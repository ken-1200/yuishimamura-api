import re

from pydantic import Field, field_validator

from ..base_schema import BaseModel


class UploadImageRequest(BaseModel):
    images: list[bytes] = Field(..., description="写真データ(base64)のリスト")
    images_json: dict = Field(..., description="写真データのJSON(写真の並び順を保持)")

    @field_validator("images")
    def validate_images(cls, v):
        image_pattern = re.compile(rb"data:image/(.*?);base64,")
        for base64_data in v:
            if not image_pattern.match(base64_data):
                raise ValueError("Invalid image data")
        return v


class UploadImageResponse(BaseModel):
    status_code: int = Field(..., description="ステータスコード")
    s3_uris: list[str] = Field(..., description="S3のURI")
