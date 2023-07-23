import json
import logging
import typing

# https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
RESERVED_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


def safe_extra(extra: dict[str, typing.Any]) -> dict[str, typing.Any]:
    """extraは予約された要素とバッティングを避ける"""
    for attr in RESERVED_ATTRS:
        if attr in extra:
            value = extra.pop(attr)
            extra[attr + "_"] = value
    return extra


# https://docs.python.org/ja/3/library/json.html#py-to-json-table
JsonSerializable = typing.Union[dict, list, tuple, str, int, float, bool, None]


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        message_obj = {
            "asctime": getattr(record, "asctime", None),
            "message": message,
            "name": record.name,
            "created": record.created,
            "msecs": record.msecs,
            "level": record.levelname,
            # https://docs.datadoghq.com/logs/log_configuration/attributes_naming_convention/#source-code
            "logger": {
                "name": record.name,
                "thread_name": record.threadName,
                "method_name": record.funcName,
                "lineno": record.lineno,
            },
        }
        message_obj.update(self.get_extra(record))
        return json.dumps(message_obj, default=self.default, ensure_ascii=False)

    def get_extra(self, record: logging.LogRecord) -> typing.Mapping:
        return {
            attr: record.__dict__[attr]
            for attr in record.__dict__
            if attr not in RESERVED_ATTRS
        }

    def default(self, obj: typing.Any) -> JsonSerializable:
        print(obj)
        return "this object can not be dumped"


def init_app(name: str, log_level: str) -> None:
    app_logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    app_logger.addHandler(handler)
    app_logger.setLevel(log_level)
