from fastapi import APIRouter

from app.interface.dto.request.update_walk_test_status_request import UpdateWalkTestStatusRequest
from app.interface.dto.response.update_walk_test_status_response import UpdateWalkTestStatusResponse

router_v2 = APIRouter(
    prefix="/v2/schedule",
    tags=["schedule"]
)

@router_v2.put("/update_walk_test_status", response_model=UpdateWalkTestStatusResponse)
async def update_walk_test_status(update_walk_test_status_request: UpdateWalkTestStatusRequest):
    pass