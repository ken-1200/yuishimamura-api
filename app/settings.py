import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Type

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from app.services.ssm import get_ssm_parameters

SSM_PARAMS = ("API_KEY",)

_parameters: Mapping[Any, str] = {}


class _SystemManagersInfo(BaseSettings):
    env: str = os.environ["APP_CONFIG_FILE"]
    REGION_NAME: str = "ap-northeast-1"
    SSM_PARAMETER_NAME_PREFIX: str = "/Production/YuiShimamuraApi/"


def ssm_source() -> Mapping[Any, str]:
    global _parameters
    if not _parameters:
        system_managers_info = _SystemManagersInfo()
        if system_managers_info.env not in ("local", "test"):
            parameters = get_ssm_parameters(
                SSM_PARAMS,
                system_managers_info.SSM_PARAMETER_NAME_PREFIX,
                system_managers_info.REGION_NAME,
            )

            converted_parameters = [
                {parameter["Name"].split("/")[-1]: parameter["Value"]}
                for parameter in parameters
                if parameter["Name"].split("/")[-1] in SSM_PARAMS
            ]
            _parameters = {
                key: value for d in converted_parameters for key, value in d.items()
            }

            # 環境変数を直接渡した場合はそちらを優先する
            # 優先度は env_file < AWS Systems Manager < 直接渡す環境変数 とする
            # pydantic は env_file と直接渡す環境変数を区別しないためこの処理が必要
            for key in _parameters.keys():
                if key in os.environ:
                    _parameters[key] = os.environ[key]

    return _parameters


class Settings(BaseSettings):
    """設定値を管理するクラス"""

    env: str = os.environ["APP_CONFIG_FILE"]
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / f"config/{env}.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    ENV_NAME: str
    DEBUG: bool
    LOG_LEVEL: str
    REGION_NAME: str
    PROFILE_NAME: str
    API_KEY: str
    ALLOW_ORIGIN_REGEX: str

    BUCKET_NAME: str
    DISTRIBUTION_ID: str

    # /docs 用のBasic認証
    BASIC_USER_NAME: str = "machidahouse-lab"
    BASIC_PASSWORD: str = "A9!h#Yn=="

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple:
        # app/config/xxx.envよりAWS Systems Managerを優先する
        return (
            init_settings,
            ssm_source,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
