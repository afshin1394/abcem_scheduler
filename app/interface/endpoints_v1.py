from fastapi import APIRouter

from app.infrastructure.schedule.trigger_update_server_list import trigger_update_server_list_dag
from app.infrastructure.schedule.trigger_update_walk_test_status import trigger_update_walk_test_dag
from app.interface.dto.request.update_walk_test_status_request import UpdateWalkTestStatusRequest
from app.interface.dto.response.speed_test_servers_response import SpeedTestsServersResponse, SpeedTestServer
from app.interface.dto.response.update_walk_test_status_response import UpdateWalkTestStatusResponse

router_v1 = APIRouter(
    prefix="/v1/schedule",
    tags=["schedule"]
)
@router_v1.put("/update_walk_test_status", response_model=UpdateWalkTestStatusResponse)
async def update_walk_test_status(update_walk_test_status_request: UpdateWalkTestStatusRequest):
    walk_test_created_response = await trigger_update_walk_test_dag(airflow_dag_id= f'update_walk_test_status_dag',walk_test_id=update_walk_test_status_request.walk_test_id,walk_test_status_id=update_walk_test_status_request.walk_test_status)
    return UpdateWalkTestStatusResponse(result=walk_test_created_response,status_code=200)

