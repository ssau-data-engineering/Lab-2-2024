from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount  # Импортируем Mount
from airflow.sensors.filesystem import FileSensor

default_args = {
    "owner" : 'ilyaswallow',
    'start_date' : datetime(2024, 11, 11),
    "retries": 1,
}

dag = DAG(
    'model_learning',
    default_args = default_args,
    description='DAG for learn model',
    schedule_interval=None,
)



# Задача 1: Загрузка и предобработка данных
load_and_preprocess = DockerOperator(
    task_id='load_and_preprocess_data',
    image="ilyaswallow/gorit",
    command="python /data/load_and_preprocess_data.py",
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

# Задача 2: Обучение модели
load_data_train_model = DockerOperator(
    task_id = 'load_data_train_model',
    image = "ilyaswallow/gorit",
    command = "python /data/load_data_train_model.py",
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

load_and_preprocess >> load_data_train_model