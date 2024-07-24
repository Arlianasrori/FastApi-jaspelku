from typing import Generic, TypeVar, Type
from pydantic import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    msg : str
    data: T