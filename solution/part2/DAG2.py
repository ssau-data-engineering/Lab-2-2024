from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'trainig_model',
    default_args=default_args,
    description='DAG for data engineering lab 2: training a neural network',
    schedule_interval=None,
)

train_model = DockerOperator(
    task_id='train_model',
    image='vmokook23/trains_model',
    command='--log_file /data/log/training_logs.txt',
    mounts=[Mount(source='/data/log', target='/data/log', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

train_model