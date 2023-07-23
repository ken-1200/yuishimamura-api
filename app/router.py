import json
import logging
import time
from collections.abc import Callable, Mapping
from functools import partial
from typing import Any

from fastapi.routing import APIRoute
from fastapi.routing import APIRouter as _APIRouter
from fastapi.routing import Request, Response

logger = logging.getLogger(__name__)


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request_headers = dict(request.headers)
            request_id = request_headers.get(
                "request-id", request_headers.get("x-amzn-trace-id")
            )
            host = str(request.client.host) if request.client else ""
            # https://docs.datadoghq.com/ja/logs/log_configuration/attributes_naming_convention/#http-requests
            http = {
                "url": str(request.url),
                "method": request.method,
                "request_id": request_id,
                "useragent": request_headers.get("user-agent"),
                "referer": request_headers.get("referer"),
            }
            setattr(request, "http", http)

            try:
                if request_headers.get("content-type") == "application/json":
                    body = self.dict_body(await request.body())
                else:
                    body = {}
                logger.info(
                    "dump request",
                    extra={
                        "http": request.http,  # type: ignore
                        "body": body,
                        "request-headers": request_headers,
                        "host": host,
                        "type": "request",
                    },
                )
            except Exception as e:
                logger.warning(e)

            before = time.time()
            response = await original_route_handler(request)
            after = time.time()
            request.http["status_code"] = response.status_code  # type: ignore
            try:
                if response.headers.get("content-type") == "application/json":
                    response_body = self.dict_body(response.body)
                else:
                    response_body = {}
                logger.info(
                    "dump response",
                    extra={
                        "http": request.http,  # type: ignore
                        "request-headers": request_headers,
                        "body": response_body,
                        "processing_time": after - before,
                        "host": host,
                        "type": "response",
                    },
                )
            except Exception as e:
                logger.warning(e)

            return response

        return custom_route_handler

    def dict_body(self, raw: bytes) -> Mapping[str, Any]:
        try:
            body = raw.decode() or "{}"
            return json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            # ファイルアップロードのバイナリデータ、不正なデータを想定
            return {"message": "dict_body() failed", "error": repr(e)}


APIRouter = partial(_APIRouter, route_class=LoggingRoute)
