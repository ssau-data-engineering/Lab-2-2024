from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

dag = DAG(
    dag_id='LAB2_TASK2',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
)

prepare_data = DockerOperator(
    task_id='prepare_data',
    image='rusekk/lab2-task2-scikit-image',
    command=f"python /data/prepare_data.py",
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

train_model = DockerOperator(
    task_id='train_model',
    image='rusekk/lab2-train-image',
    command=f"python /data/train_model.py",
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

prepare_data >> train_model