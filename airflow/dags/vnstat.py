from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

vnstat_dag = DAG(
    dag_id="vnstat",
    schedule="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
)


task1 = BashOperator(
    task_id="vnstat_starting", bash_command="vnstat -d", dag=vnstat_dag
)


task2 = BashOperator(
    task_id="vnstat_ending",
    bash_command="vnstat -i eth0",
    dag=vnstat_dag,
)

task1 >> task2
