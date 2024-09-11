from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

import csv, logging
# Lớp này được sử dụng để tạo tạm thời các tệp tin mà tự động được xóa khi chúng không còn được sử dụng.
from tempfile import NamedTemporaryFile

default_args = {
    'owner': 'vohoang',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

def postgres_to_s3(ds_nodash, next_ds_nodash):
    # step 1: query data từ postgresql db
        # Truy cập vào airflow scheduler container và kiểm tra version của postgres package bằng lệnh pip list | grep postgres
        # Vào documentation tìm đến postgress và chọn version package phù hợp để xem api: https://airflow.apache.org/docs/ và chọn python API
        # https://airflow.apache.org/docs/apache-airflow-providers-postgres/5.11.1/_api/airflow/providers/postgres/hooks/postgres/index.html
        # Tạo postgres_conn_id trong connection airflow
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders where date >= %s and date <= %s", (ds_nodash, next_ds_nodash))
    # Task sẽ được thực thi lặp lại nên cần phải cung cấp 1 tên động cho file => Sử dụng marco trong airflow (h là template trong airflow)
    
    with NamedTemporaryFile(mode='w', suffix= f"{ds_nodash}") as f:
    # with open(f"dags/get_orders_{ds_nodash}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info("Saved orders data in text file: %s", f"dags/get_orders_{ds_nodash}.txt")
    # step 2: upload text file into S3
        # Làm tương tự như ở trên để tìm version của amazon package: pip list | grep amazon
        s3_hook = S3Hook(aws_conn_id="minio_s3_conn")
        s3_hook.load_file(
            filename=f.name,
            key=f"orders/{ds_nodash}.txt",
            bucket_name="airflow",
            replace=True  # replace file nếu nó đã tồn tại
        )
        logging.info("Orders file %s has been pushed to S3!", f.name)
    

with DAG(
    dag_id="dag_with_postgers_hooks_v04",
    default_args=default_args,
    start_date=datetime(2022, 4, 30),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id="postgres_to_s3",
        python_callable=postgres_to_s3
    )
    task1