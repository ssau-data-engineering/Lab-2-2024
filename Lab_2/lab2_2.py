from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 24),
    'retries': 1,
}

dag = DAG(
    'Data_eng_2.2',
    default_args=default_args,
    description='Training a neural network',
    schedule_interval=None,
)

read_data = DockerOperator(
    task_id='read_data',
    image='dekartvon/ml_container_3',
    command='python /data/read_data.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

train_model = DockerOperator(
    task_id='train_model',
    image='dekartvon/ml_container_3',
    command='python /data/train_model.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

read_data >> train_model
