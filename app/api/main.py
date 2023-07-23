from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from app.constants import API_KEY_NAME
from app.settings import Settings

from .delete_update_images.views import router as delete_update_images_router
from .upload_images.views import router as upload_images_router

settings = Settings()


async def get_api_key(
    api_key_header: str = Security(APIKeyHeader(name=API_KEY_NAME, auto_error=False))
) -> str:
    """APIキーによるクライアントの簡易認証

    APIエンドポイントのみを対象とし、ヘルスチェックやAPIドキュメントは対象外とする
    """
    if api_key_header in settings.API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


router = APIRouter(
    dependencies=[Depends(get_api_key)],
)
router.include_router(delete_update_images_router)
router.include_router(upload_images_router)
