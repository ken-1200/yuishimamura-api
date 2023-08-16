import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


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
