import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from airflow.sensors.python import PythonSensor
import os

dag = DAG(
    dag_id="LR_2_task_2",
    schedule="0 0 * * *", 
    start_date=datetime.datetime(2024, 10, 27, tzinfo=datetime.timezone.utc), 
    catchup=False,  
    dagrun_timeout=datetime.timedelta(minutes=60),  
    tags=["LR"],
)

path = "./data/LR_2_task2/"


def check_new_folders():
    target_folder = os.path.join(path, 'data')
    return os.path.isdir(target_folder)


wait_for_new_file = PythonSensor(
        task_id='wait_files',
        python_callable = check_new_folders,
        poke_interval=10,  
        timeout=200,
        mode='poke',
        dag=dag,
    )


read_data = DockerOperator(
    task_id='read_data',
    image='gr0mozeka/my_image:v1.0', 
    command='python /data/LR_2_task2/read_data.py --input /data --output /prepared_data',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

train_model = DockerOperator(
    task_id='train_model',
    image='gr0mozeka/train_model_image:v1.0',
    command='python /data/LR_2_task2/train_model.py --input /prepared_data --output /trained_model',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

wait_for_new_file >> read_data >> train_model