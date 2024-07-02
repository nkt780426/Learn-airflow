Nguồn: 
    https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
Chạy:
docker compose up airflow-init
docker compose up -d

Dừng
docker compose down -v

Chạy minio:
mkdir -p ./minio/data
docker run \
    -p 9000:9000 \
    -p 9001:9001 \
    --name minio \
    -v ./minio/data:/data \
    -e "MINIO_ROOT_USER=ROOTNAME" \
    -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
    quay.io/minio/minio server /data --console-address ":9001"