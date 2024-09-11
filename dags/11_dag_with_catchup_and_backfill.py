from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'vohoang',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

# Catchup

# with DAG(
#     dag_id='dag_with_catchup_and_backfill_v01',
#     default_args=default_args,
#     start_date=datetime(2024, 6, 27), # Hiện tại đang là 1/7, khi click hoạt DAG và nhấn refresh sẽ thấy 4 task được chạy => Đại diện cho 4 ngày đã bỏ lỡ
#     schedule_interval='@daily',
#     catchup=True
# ) as dag:
#     task1 = BashOperator(
#         task_id='task1',
#         bash_command='echo "This is a simple bash command!"'
#     )

# Backfill: Giả sử DAG đã được kích hoạt và đang hoạt động bình thường. Tuy nhiên bạn vừa mới update lại DAG và muốn chạy lại các DAG đã update lại với các ngày trước đó => Sử dụng backfill command trong bash của container scheduler
# Sử dụng docker ps tìm id của container scheduler và mở bash nó ra: docker exec -it 84781f63fb71 bash
# Chạy lệnh "airflow dags backfill -s 2024-11-01 -e 2024-11-08" (-s laf start date, -e là enđate)

with DAG(
    dag_id='dag_with_catchup_and_backfill_v03',
    default_args=default_args,
    start_date=datetime(2024, 6, 27), # Hiện tại đang là 1/7, khi click hoạt DAG và nhấn refresh sẽ thấy 4 task được chạy => Đại diện cho 4 ngày đã bỏ lỡ
    schedule_interval='@daily',
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "This is a simple bash command!"'
    )
