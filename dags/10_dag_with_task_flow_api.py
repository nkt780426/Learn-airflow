from airflow.decorators import dag, task
from datetime import datetime, timedelta
default_agrs = {
    'owner' : 'vohoang',
    'retries': 5,
    'retry_delay' : timedelta(minutes=5)
}

@dag(
    dag_id='dag_with_workflow_api_v02',
    default_args=default_agrs,
    start_date=datetime(2024, 6, 30),
    schedule_interval='@daily'
)
def hello_world_etl():
    
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name' : 'vo',
            'last_name' : 'hoang'
        }

    @task()
    def get_age():
        return 22
    
    @task()
    def greet(first_name, last_name, age):
        print(f'Hello world. My name is {first_name} {last_name} and I am {age} years old!')
    
    # Taskflow API tự động tính toán workflow cho chúng ta, không cần phải set downstream như trước
    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], last_name=name_dict['last_name'], age=age)
    
greet_dag = hello_world_etl()