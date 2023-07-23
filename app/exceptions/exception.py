from enum import Enum
from typing import Any

from fastapi.exceptions import RequestValidationError


class ErrorCode(Enum):
    """エラーレスポンス内の message 要素と code 要素に対応"""

    InternalServerError = "internal_server_error"
    NotFound = "not_found"
    UpstreamError = "upstream_error"
    ValidationError = "validation_error"
    S3UploadError = "s3_upload_error"
    S3GetObjectError = "s3_get_object_error"
    S3DeleteObjectError = "s3_delete_object_error"


class YuishimamuraAPIBaseException(Exception):
    """エラー内容を表現するクラス"""

    service_name: str = "yuishimamura_api"
    status_code: int = 500
    code: ErrorCode = ErrorCode.InternalServerError

    def __init__(self, **options: Any) -> None:
        """レスポンスの追加要素をキーワード引数で受け取る

        キーワード引数で渡した値がそのまま追加要素としてレスポンスボディに含まれます
        JSONシリアライズ可能な値のみ受け付けます
        """
        self.options = options

    @property
    def content(self) -> dict:
        """エラー時のレスポンスボディを返す"""
        content = {
            "code": f"{self.service_name}.{self.code.value}",
            "message": self.code.name,
        }
        if self.options:
            return dict(**content, **self.options)
        else:
            return content


class ValidationError(YuishimamuraAPIBaseException):
    """リクエストのバリデーションチェックがエラーの場合に返す

    :errors: pydantic が生成するエラー内容がそのまま格納される
    """

    status_code = 400
    code = ErrorCode.ValidationError

    def __init__(self, exc: RequestValidationError) -> None:
        super().__init__(errors=exc.errors())


class S3UploadError(YuishimamuraAPIBaseException):
    """S3にアップロードできなかった場合に返す

    :body: エラー内容をそのまま格納する
    """

    status_code = 400
    code = ErrorCode.S3UploadError

    def __init__(self, body: dict) -> None:
        super().__init__(body=body)


class S3GetObjectError(YuishimamuraAPIBaseException):
    """S3上のオブジェクトを取得できなかった場合に返す

    :body: エラー内容をそのまま格納する
    """

    status_code = 400
    code = ErrorCode.S3GetObjectError

    def __init__(self, body: dict) -> None:
        super().__init__(body=body)


class S3DeleteObjectError(YuishimamuraAPIBaseException):
    """S3上のオブジェクトを削除できなかった場合に返す

    :body: エラー内容をそのまま格納する
    """

    status_code = 400
    code = ErrorCode.S3DeleteObjectError

    def __init__(self, body: dict) -> None:
        super().__init__(body=body)


class NotFound(YuishimamuraAPIBaseException):
    """対象が見つからない場合に返す

    exception_handler 以外では基本的に使わない
    """

    status_code = 404
    code = ErrorCode.NotFound

    def __init__(self) -> None:
        super().__init__()


class UpstreamError(YuishimamuraAPIBaseException):
    """外部システムからエラーが返ってきた場合に返す

    PDF生成APIやSalesforceなどを想定しています

    :url: Invoice API からのリクエスト先URL
    :body: 外部システムからのレスポンス
    """

    code = ErrorCode.UpstreamError

    def __init__(self, status_code: int, url: str, body: dict) -> None:
        super().__init__(url=url, body=body)
        self.status_code = status_code
