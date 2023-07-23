from pydantic import Field

from ..base_schema import BaseModel


class UploadImageRequest(BaseModel):
    images: list[bytes] = Field(..., description="写真データ(base64)のリスト")
    images_json: dict = Field(..., description="写真データのJSON(写真の並び順を保持)")


class UploadImageResponse(BaseModel):
    status_code: int = Field(..., description="ステータスコード")
    s3_uris: list[str] = Field(..., description="S3のURI")
