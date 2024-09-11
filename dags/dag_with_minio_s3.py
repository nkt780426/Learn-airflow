from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'vohoang',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

with DAG(
    dag_id='dag_with_minio_s3_v04',
    default_args=default_args,
    start_date=datetime(2024, 6, 30),
    schedule='@daily'
) as dag:
    # Sensor operator để check sự tồn tại của 1 file hay cái gì đó
    task1 = S3KeySensor(
        task_id = 'sensor_minio_s3',
        bucket_name = 'airflow',
        bucket_key = 'data.csv',
        aws_conn_id = 'minio_s3_conn',
        # poke là default mode của sensor operator
        # poke như kiểu mỗi 5s sẽ check sự tồn tại của file, có thể điều chỉnh nó
        mode='poke',
        poke_interval=5,    # mặc định 30s giờ chuyển thành 5s
        timeout=30
    )