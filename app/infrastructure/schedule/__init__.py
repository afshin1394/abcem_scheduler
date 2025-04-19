from fastapi import HTTPException
from httpx import BasicAuth

from app.core.config import settings
from app.infrastructure.di import get_http_client


async def unpause_dag(airflow_dag_id: str) -> None:
    url = f"{settings.airflow_base_url}dags/{airflow_dag_id}"
    payload = {"is_paused": False}
    auth = BasicAuth("admin", "admin123")
    client = await get_http_client()

    response = await client.patch(url, json=payload, auth=auth)
    print(f"Unpause DAG response: {response.status_code} -> {response.text}")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to unpause DAG: {response.text}")
