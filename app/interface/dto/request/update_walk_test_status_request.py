from pydantic import BaseModel

from app.infrastructure.dags.update_walk_test_status_dag import WalkTestStatusEnum


class UpdateWalkTestStatusRequest(BaseModel):
    walk_test_id: str
    walk_test_status: WalkTestStatusEnum