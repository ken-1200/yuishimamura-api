import logging
import sys
import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from .exception import NotFound, ValidationError, YuishimamuraAPIBaseException

logger = logging.getLogger(__name__)


def init_app(app: FastAPI) -> None:
    # 例外ハンドラの登録
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(YuishimamuraAPIBaseException, default_invoice_api_handler)
    app.add_exception_handler(Exception, default_handler)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """リクエストパラメータのバリデーションエラーハンドラー"""
    return await default_invoice_api_handler(request, ValidationError(exc))


async def not_found_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """404のエラーハンドラー"""
    return await default_invoice_api_handler(request, NotFound())


async def default_invoice_api_handler(
    request: Request, exc: YuishimamuraAPIBaseException
) -> JSONResponse:
    status_code = exc.status_code
    content = exc.content
    dump_error_response(request, status_code, content)
    return JSONResponse(status_code=status_code, content=content)


async def default_handler(request: Request, exc: Exception) -> JSONResponse:
    # ここは予期せぬエラー以外では基本的に呼ばれない想定
    # 呼ばれていたら即座に修正すること
    t, v, tb = sys.exc_info()
    extra = {
        "kind": repr(exc),
        "message": "Please contact the maintainers because this error was not handled",
        "stack": "".join(traceback.format_exception(t, v, tb)),
    }
    # 基本的には app.router で付与済み
    http = getattr(request, "http", {})
    logger.error(repr(exc), extra={"error": extra, "http": http})

    error = YuishimamuraAPIBaseException()
    status_code = error.status_code
    content = error.content
    response = JSONResponse(status_code=status_code, content=content)
    dump_error_response(request, status_code, content)
    return response


def dump_error_response(request: Request, status_code: int, body: dict) -> None:
    # https://docs.datadoghq.com/ja/logs/log_configuration/attributes_naming_convention/#http-requests
    request_headers = request.headers
    host = str(request.client.host) if request.client else ""
    if getattr(request, "http", {}):
        request.http["status_code"] = status_code  # type: ignore
    else:
        http = {
            "url": str(request.url),
            "method": request.method,
            "request_id": request_headers.get("x-amzn-trace-id"),
            "useragent": request_headers.get("user-agent"),
            "referer": request_headers.get("referer"),
            "status_code": status_code,
        }
        setattr(request, "http", http)
    try:
        logger.info(
            "dump response",
            extra={
                "http": request.http,  # type: ignore
                "request-headers": request_headers,
                "body": body,
                "host": host,
                "type": "response",
            },
        )
    except Exception as e:
        logger.warning(e)
