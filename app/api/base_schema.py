from pydantic import BaseModel as BaseModel_
from pydantic import ConfigDict


class BaseModel(BaseModel_):
    model_config = ConfigDict(extra="forbid")
