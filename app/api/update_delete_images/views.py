from fastapi import Depends, Request

from app.router import APIRouter

from .schema import UpdateDeleteImageRequest, UpdateDeleteImageResponse
from .use_cases import UpdateDeleteImage

router = APIRouter()


@router.post(
    "/update_delete_images",
    summary="写真並び替え・削除API",
    response_model=UpdateDeleteImageResponse,
)
async def update_delete_images(
    request: Request,
    data: UpdateDeleteImageRequest,
    use_case: UpdateDeleteImage = Depends(UpdateDeleteImage),
) -> UpdateDeleteImageResponse:
    """写真並び替え・削除API"""
    return UpdateDeleteImageResponse(**await use_case.execute(data))
