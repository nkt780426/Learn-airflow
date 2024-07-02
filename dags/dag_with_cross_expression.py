from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'vohoang',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_cross_expression_v03',
    default_args=default_args,
    start_date=datetime(2024, 6, 25),
    schedule_interval='0 3 * * Tue-Thu'    
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "dag with cron expression"'
    )
    
    task1