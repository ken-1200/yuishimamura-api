from pydantic import BaseModel as BaseModel_
from pydantic import Extra


class BaseModel(BaseModel_):
    class Config:
        extra = Extra.forbid
