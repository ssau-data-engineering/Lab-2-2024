from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

# Параметры по умолчанию для DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'data_engineering_lab_2',
    default_args=default_args,
    description='DAG for data engineering lab 2: training a neural network',
    schedule_interval=None,  # Это означает, что DAG будет запускаться вручную
    catchup=False,  # Исключаем выполнение DAG для прошлых дат
)

# Оператор для чтения данных
read_data = DockerOperator(
    task_id='read_data',
    image='snail911/read_data_image:v3',
    command='python /app/read_data.py --input /data/raw --output /data/prepared',
    mounts=[Mount(source='/data/raw', target='/data/raw', type='bind'),
            Mount(source='/data/prepared', target='/data/prepared', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

# Оператор для тренировки модели
train_model = DockerOperator(
    task_id='train_model',
    image='snail911/train_model_image',
    command='python /app/train_model.py --input /data/prepared --output /data/trained',
    mounts=[
        Mount(source='/data/prepared', target='/data/prepared', type='bind'),
        Mount(source='/data/trained', target='/data/trained', type='bind')
    ],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

# Описание порядка выполнения задач
read_data >> train_model
