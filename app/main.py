import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import HTMLResponse, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from mangum import Mangum

from app.api.main import router as api_router
from app.exceptions.exception_handler import init_app as init_exception_handler
from app.log import init_app as init_log
from app.settings import Settings

settings = Settings()
security = HTTPBasic()

app = FastAPI(title="Yuishimamura API", docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")

# 例外ハンドラの登録
init_exception_handler(app)

# ログ設定
init_log("app", settings.LOG_LEVEL)


@app.get("/", include_in_schema=False)
@app.get("/health", include_in_schema=False)
async def health() -> JSONResponse:
    """ヘルスチェック"""
    return JSONResponse({"message": "It worked!!"})


@app.get("/docs", include_in_schema=False)
async def get_documentation(
    credentials: HTTPBasicCredentials = Depends(security),
) -> HTMLResponse:
    if not _validate_credentials(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(
    credentials: HTTPBasicCredentials = Depends(security),
) -> JSONResponse:
    if not _validate_credentials(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return JSONResponse(
        get_openapi(
            title="Yui Shimamura API(Ver1.0)",
            version="1.0",
            routes=app.routes,
        )
    )


def _validate_credentials(credentials: HTTPBasicCredentials) -> bool:
    correct_username = secrets.compare_digest(
        credentials.username, settings.BASIC_USER_NAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.BASIC_PASSWORD
    )
    return correct_username and correct_password


# FastAPIのインスタンスをMangumのコンストラクタに渡して、handlerとして読めるようにしておく
handler = Mangum(app, "off")  # type: ignore

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
