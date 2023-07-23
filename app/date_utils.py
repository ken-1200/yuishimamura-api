import time
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pytz import timezone as tz


def get_jst_now() -> datetime:
    """JST現在日時"""
    return datetime.now(tz("Asia/Tokyo"))


def get_utc_now() -> datetime:
    """UTC現在日時"""
    return datetime.now(tz("UTC"))


def get_first_day_of_month(dt: datetime) -> datetime:
    """月の初日を取得"""
    return dt.replace(day=1)


def get_23rd_of_month(dt: datetime) -> datetime:
    """月の23日を取得"""
    return dt.replace(day=23)


def get_last_day_of_month(dt: datetime) -> datetime:
    """月の末日を取得"""
    return (dt + relativedelta(months=1)).replace(day=1) - timedelta(days=1)


def make_time_ns() -> int:
    """ナノ秒のタイムスタンプを生成"""
    return time.time_ns()


def make_y_m_str_slash(dt: datetime) -> str:
    """YYYY/mm形式に変換"""
    return datetime.strftime(dt, "%Y/%m")


def make_y_m_d_str_slash(date: datetime) -> str:
    """YYYY/mm/dd形式に変換"""
    return datetime.strftime(date, "%Y/%m/%d")


def make_ymd_str(date: datetime) -> str:
    """YYYYmmdd形式に変換"""
    return datetime.strftime(date, "%Y%m%d")


def make_y_m_d_str(date_str: str) -> str:
    """YYYY/mm/dd形式からYYYY-mm-dd形式の日時を作成"""
    return datetime.strptime(date_str, "%Y/%m/%d").strftime("%Y-%m-%d")


def convert_to_timezone(dt: datetime, timezone: str) -> datetime:
    """datetimeを指定したタイムゾーンに変換"""
    return dt.astimezone(tz(timezone))
