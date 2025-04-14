from datetime import timedelta, datetime

from enum import Enum
import requests

from airflow import DAG
from airflow.operators.python import PythonOperator


class WalkTestStatusEnum(int,Enum):
    created = 1
    deprecated = 2
    done = 3

def call_update_walk_test_status(walk_test_id: str, status: WalkTestStatusEnum, api_base_url: str = "http://core:8001"):
    response = requests.put(
        f"{api_base_url}/v1/walk_test/update_walk_test_status",
        json={
            "walk_test_id": walk_test_id,
            "walk_test_status": status.value
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()

    if response.status_code == 204:
        print("Update successful, no content.")
        return None
    return response.json()




def wrapper(**kwargs):
    conf = kwargs['dag_run'].conf
    walk_test_id = conf.get('walk_test_id')
    walk_test_status_id = int(conf.get('walk_test_status_id'))
    call_update_walk_test_status(walk_test_id, WalkTestStatusEnum(walk_test_status_id))


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    dag_id='update_walk_test_status_dag',
    default_args=default_args,
    description='Marks walk test as deprecated 5 seconds after creation',
    schedule_interval=None,
    catchup=False,
    tags=['walk_test'],
)

PythonOperator(
    task_id='mark_status_deprecated',
    python_callable=wrapper,
    provide_context=True,
    dag=dag,
)