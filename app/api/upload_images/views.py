from fastapi import Depends, Request

from app.router import APIRouter

from .schema import UploadImageRequest, UploadImageResponse
from .use_cases import UploadImage

router = APIRouter()


@router.post(
    "/upload_images", summary="写真アップロードAPI", response_model=UploadImageResponse
)
async def upload_images(
    request: Request,
    data: UploadImageRequest,
    use_case: UploadImage = Depends(UploadImage),
) -> UploadImageResponse:
    """写真アップロードAPI"""
    return UploadImageResponse(**await use_case.execute(data))
