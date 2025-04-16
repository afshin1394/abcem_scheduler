import asyncio
from datetime import datetime, timedelta
from typing import List

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from pydantic import BaseModel



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




SPEEDTEST_API_URL = "https://www.speedtest.net/api/js/servers?engine=js&https_functional=true&search=Iran"

def get_iran_speedtest_servers() -> List[SpeedTestServer]:
    response = requests.get(
        SPEEDTEST_API_URL,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()

    if response.status_code == 204:
        print("No content returned from speedtest API.")
        return []

    raw_servers = response.json()

    return [
        SpeedTestServer(
            id=s["id"],
            name=s["name"],
            sponsor=s["sponsor"],
            host=s["host"],
            country=s["country"],
            lat=s["lat"],
            lon=s["lon"],
            distance=s.get("distance", 0),
            url=s.get("url", "")
        )
        for s in raw_servers
    ]

def call_update_server_lists(servers: List[SpeedTestServer], api_base_url: str = "http://core:8001"):
    payload = {
        "servers": [server.model_dump() for server in servers]
    }

    response = requests.post(
        f"{api_base_url}/v1/speed_test/update_servers",
        json=payload,
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    print(f'{api_base_url}/v1/speed_test/update_servers')

    response.raise_for_status()

    if response.status_code == 204:
        print("Update successful, no content.")
        return None

    return response.json()




if __name__ == "__main__":
    call_update_server_lists(get_iran_speedtest_servers())

def update_speed_test_servers():
    servers = get_iran_speedtest_servers()
    call_update_server_lists(servers)
    return servers

def wrapper(**kwargs):
    update_speed_test_servers()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    dag_id='update_speed_test_servers_daily_dag',
    default_args=default_args,
    description='Speed test servers would be updated every 24 hours',
    schedule='@daily',  # Set to run daily at midnight
    catchup=False,
    tags=['speed_test_servers'],
)
PythonOperator(
    task_id='update_speed_test_servers_daily_in_core',
    python_callable=wrapper,
    dag=dag,
)