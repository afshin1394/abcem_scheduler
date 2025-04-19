from pydantic import BaseModel

from app.interface.dto.success_response import BaseSuccessResponse

class SpeedTestServer(BaseModel):
    id: int
    name: str
    sponsor: str
    host: str
    country: str
    lat: float
    lon: float
    distance: float
    url: str


class SpeedTestsServersResponse(BaseSuccessResponse[list[SpeedTestServer]]):
    pass