from airflow import DAG
from datetime import timedelta, datetime

from airflow.operators.python import PythonOperator
default_args = {
    'owner': 'vohoang',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

# # ti=task instance
# def greet(age, ti):
#     name = ti.xcom_pull(task_ids='get_name')
#     print(f"Hello world! My name is {name}, and I am {age} years old!")

# def greet(age, ti):
#     first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
#     last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
#     print(f"Hello world! My name is {first_name} {last_name}, and I am {age} years old!")

def get_age(ti):
    ti.xcom_push(key='age', value=19)

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age=ti.xcom_pull(task_ids='get_age', key='age')
    print(f"Hello world! My name is {first_name} {last_name}, and I am {age} years old!")

# Theo mặc định, tát cả function return giá trị sẽ được lưu vào xcom (hình 9.xcom)
def get_name(ti):
    ti.xcom_push(key='first_name', value='Vo')
    ti.xcom_push(key='last_name', value='Hoang')
    
with DAG(
    dag_id='xcom_dag_v03',
    description='our_first_dag_using_python_operator',
    default_args=default_args,
    start_date=datetime(2024, 6, 30),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
        # kwargs={'age' :20}
    )
    
    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    
    task3=PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    [task2, task3] >> task1