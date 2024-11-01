from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 28),
    'retries': 1,
}

dag = DAG(
    'data_engineering_lab_2',
    default_args=default_args,
    description='DAG for data engineering lab 2: training a neural network',
    schedule_interval=None,
)

read_data = DockerOperator(
    task_id='read_data',
    image='chitorkinegor/read-data-image',
    command='python /data/read_data.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

train_model = DockerOperator(
    task_id='train_model',
    image='chitorkinegor/train-model-image',
    command='python /data/train_model.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

read_data >> train_model
