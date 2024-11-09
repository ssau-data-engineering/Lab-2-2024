import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

dag = DAG(
    'data_engineering_lab_2_2',
    description='DAG for data engineering lab 2: training a neural network',
    schedule_interval=None,
    dagrun_timeout=datetime.timedelta(minutes=40),
    start_date=datetime.datetime(2024, 1, 1),
    catchup=False,
)

check = DockerOperator(
    task_id='check_data',
    image='irameis/dat-eng:cnn',
    command='python /data/check.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

train_model = DockerOperator(
    task_id='train_model',
    image='irameis/dat-eng:cnn',
    command='python /data/train.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

check >> train_model