from typing import Generic, TypeVar, Optional
from pydantic import Field, BaseModel

# A type variable for the data we're returning
DataT = TypeVar("DataT")


class BaseSuccessResponse(BaseModel, Generic[DataT]):
    """
    A generic success response model with a default HTTP 200 status code
    and a 'result' that can be any type or model.
    """
    status_code: int = Field(200, description="HTTP status code, defaults to 200")
    latency: Optional[float] = Field(0, description="Latency (in seconds)")
    result: Optional[DataT] = Field(description="Actual data returned by the endpoint")
