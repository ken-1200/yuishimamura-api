from fastapi import Depends, Request

from app.router import APIRouter

from .schema import DeleteUpdateImageRequest, DeleteUpdateImageResponse
from .use_cases import DeleteUpdateImage

router = APIRouter()


@router.post(
    "/delete_update_images",
    summary="写真削除・並び替えAPI",
    response_model=DeleteUpdateImageResponse,
)
async def delete_update_images(
    request: Request,
    data: DeleteUpdateImageRequest,
    use_case: DeleteUpdateImage = Depends(DeleteUpdateImage),
) -> DeleteUpdateImageResponse:
    """写真削除・並び替えAPI"""
    return DeleteUpdateImageResponse(**await use_case.execute(data))
