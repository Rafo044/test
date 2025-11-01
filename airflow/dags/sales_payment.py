"""Imports"""

from datetime import datetime

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator
from airflow.decorators import task_group
import pandas as pd

from authentification import authenticate

# =====================================================================
#                     DAG
# ====================================================================

sales_payment = DAG(
    dag_id="sales_payment",
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
)

# =====================================================================
#                    HELPER FUNCTIONS
# ====================================================================


def load_data(**context):
    """
    Restapi dan datanı çəkən funksiya.
    """
    response = authenticate(GET, "all")
    if response.status_code == 200:
        data = response.json()
        context["ti"].xcom_push(key="data", value=data)
    else:
        raise Exception(f"Failed to load data: {response.status_code}")


def read_data(**context):
    """
    Datani temizleyen funksiya.
    """
    data = context["ti"].xcom_pull(key="data")
    read_data = pd.DataFrame(data)
    context["ti"].xcom_push(key="data", value=read_data)


def clean_data(**context):
    """
    Datani temizleyen funksiya.
    """
    data = context["ti"].xcom_pull(key="data", value=read_data)
    clean_data = data.dropna()
    context["ti"].xcom_push(key="data", value=clean_data)


# ====================================================================
#                     TASKS
# ====================================================================


@task_group(group_id="load_data")
def load_data_task():
    task2 = EmptyOperator(task_id="waiting_load_data")
    task3 = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )
    task2 >> task3


@task_group(group_id="read_data")
def read_data_task():
    task4 = EmptyOperator(task_id="waiting_read_data")
    task5 = PythonOperator(
        task_id="read_data",
        python_callable=read_data,
    )
    task4 >> task5


@task_group(group_id="clean_data")
def clean_data_task():
    task6 = EmptyOperator(task_id="waiting_clean_data")
    task7 = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data,
    )
    task6 >> task7


load_data_task() >> read_data_task() >> clean_data_task()
