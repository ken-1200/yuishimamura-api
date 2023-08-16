from pydantic import Field, field_validator

from ..base_schema import BaseModel


class UpdateDeleteImageRequest(BaseModel):
    images_path: list[str] = Field(..., description="写真保存先のパス(S3)")
    images_json: dict = Field(..., description="写真データのJSON(写真の並び順を保持)")

    @field_validator("images_path")
    def validate_images_path(cls, v):
        for path in v:
            if not path.startswith("s3://") or not path.endswith(".webp"):
                raise ValueError(
                    "images_path needs to start with s3:// and end with .webp"
                )
        return v


class UpdateDeleteImageResponse(BaseModel):
    status_code: int = Field(..., description="ステータスコード")
    s3_uris: list[str] = Field(..., description="S3のURI")
