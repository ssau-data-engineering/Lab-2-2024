from datetime import datetime, timedelta, timezone
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 30, tzinfo=timezone.utc),
    'retries': 1,
}


dag = DAG(
    'training_dag',
    default_args=default_args,
    description='DAG for training model',
    schedule_interval=None,
)


prepare_data = DockerOperator(
    task_id='prepare_data',
    image='marelli0/my_tensorflow_image:1.0',
    command='python /data/prepare_data.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

train_model = DockerOperator(
    task_id='train_model',
    image='marelli0/my_tensorflow_image:1.0',
    command='python /data/train_model.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

prepare_data >> train_model