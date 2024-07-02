from airflow import DAG
from datetime import timedelta, datetime

from airflow.operators.python import PythonOperator
default_args = {
    'owner': 'vohoang',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

# function muốn chạy
def greet(name, age):
    print(f"Hello world! My name is {name}, and I am {age} years olds!")

with DAG(
    dag_id='our_dag_with_python_operator_v01',
    description='our_first_dag_using_python_operator',
    default_args=default_args,
    start_date=datetime(2024, 6, 30),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        # Nếu hàm có biến đầu vào như trên thì sử dụng thêm thuộc tính op_kwargs
        op_kwargs={'name': 'Vo', 'age': 20}
    )