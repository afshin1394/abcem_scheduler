
from fastapi import HTTPException
from httpx import BasicAuth

from app.core.config import settings
from app.infrastructure.dags.update_walk_test_status_dag import WalkTestStatusEnum
from app.infrastructure.di import get_http_client
from app.infrastructure.schedule import unpause_dag


async def trigger_update_walk_test_dag(airflow_dag_id: str, walk_test_id: str,
                                       walk_test_status_id: WalkTestStatusEnum) -> str:
    await unpause_dag(airflow_dag_id)

    dag_run_id = f"{airflow_dag_id}__{walk_test_id}"  # ensure unique run_id

    payload = {
        "dag_run_id": dag_run_id,
        "conf": {
            "walk_test_id": walk_test_id,
            "walk_test_status_id": walk_test_status_id
        }
    }

    print(f"url of dag run:->>>>>>>>>>>>>>>>>>>>> {settings.airflow_base_url}dags/{airflow_dag_id}/dagRuns")
    auth = BasicAuth("admin", "admin123")
    client = await get_http_client()
    response = await client.post(
        f"{settings.airflow_base_url}dags/{airflow_dag_id}/dagRuns",
        auth=auth,
        json=payload,
    )
    print(f"trigger_update_walk_test_dag response.status_code ->>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {response.status_code}")
    if response.status_code not in (200, 201):  # allow both
        raise HTTPException(status_code=500, detail=f"Failed to trigger DAG: {response.text}")

    return dag_run_id
