from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'vohoang',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

# function muốn chạy
def get_sklearn():
    import sklearn
    print(f"scikit-learn with version {sklearn.__version__}")

with DAG(
    dag_id='our_dag_with_python_dependence_v01',
    description='our_first_dag_using_python_operator',
    default_args=default_args,
    start_date=datetime(2024, 6, 30),
    schedule_interval='@daily'
) as dag:
    get_sklearn = PythonOperator(
        task_id='get_sklearn',
        python_callable=get_sklearn,
    )
    
    get_sklearn