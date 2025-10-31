"""FastAPI servisinin authentikifasiyasını yoxlanması"""

import os
import requests
from dotenv import load_dotenv


from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sdk import DAG
import pendulum

load_dotenv()

TOKEN = os.getenv("TOKEN")
FASTAPI_URL = os.getenv("FASTAPI_URL")

authentification = DAG(
    dag_id="authentification",
    start_date=pendulum.datetime(2023, 1, 1),
    schedule="@once",
)


def authenticate():
    """FastAPI servisinin authentikifasiyasını yoxlama funksiyası
    Returns:
        Success: Autentifikasiya uygurludur.
        Failure: Autentifikasiya yalnışdır.
    """
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(FASTAPI_URL, headers=headers)

    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed:", response.status_code, response.json())


task = PythonOperator(
    task_id="authenticate",
    python_callable=authenticate,
    dag=authentification,
)

trigger_run = TriggerDagRunOperator(
    task_id="trigger_run",
    dag=authentification,
    trigger_dag_id="sales_payment",
    trigger_run_id="sales_payment_run",
)

task >> trigger_run
