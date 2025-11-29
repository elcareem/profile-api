from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class ResponseModel(GenericModel, Generic[T]):
    status: bool
    data: T
    message: str

def response(data: T, message: str = "Request successful") -> ResponseModel[T]:
    """
    Wraps a Pydantic model into a validated ResponseModel.
    """
    return ResponseModel(
        status=True,
        data=data,
        message=message
    )

