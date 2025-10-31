from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator
from airflow.decorators import task_group
from datetime import datetime


sales_payment = DAG(
    dag_id="sales_payment",
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
)


@task_group(group_id="wait_for_auth")
def wait_for_auth():
    task1 = EmptyOperator(task_id="wait_for_auth")
