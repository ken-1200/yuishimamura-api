from pydantic import Field

from ..base_schema import BaseModel


class DeleteUpdateImageRequest(BaseModel):
    images_path: list[str] = Field(..., description="写真保存先のパス(S3)")
    images_json: dict = Field(..., description="写真データのJSON(写真の並び順を保持)")


class DeleteUpdateImageResponse(BaseModel):
    status_code: int = Field(..., description="ステータスコード")
    s3_uris: list[str] = Field(..., description="S3のURI")
