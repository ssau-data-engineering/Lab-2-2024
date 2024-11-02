from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount 

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 11, 2),
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
    image='vasser232/read-data',
    command='/app/input/data /app/output/prepared_data',
    mounts=[
        Mount(source='/data/neural_model', target='/app/input', type='bind'),
        Mount(source='/data/neural_model', target='/app/output', type='bind')
    ],
    auto_remove=True,
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)


train_model = DockerOperator(
    task_id='train_model',
    image='vasser232/train-model',
    command=[
        '--train-dir', '/data/input/prepared_data/train',  
        '--val-dir', '/data/input/prepared_data/val',      
        '--output-dir', '/data/output/checkpoints',         
        '--batch-size', '8',
        '--num-workers', '4',
        '--epochs', '10',
    ],
    mounts=[
        Mount(
            source='/data/neural_model',  
            target='/data/input',         
            type='bind'
        ),
        Mount(
            source='/data/neural_model',  
            target='/data/output',        
            type='bind'
        )
    ],
    auto_remove=True,
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

read_data >> train_model
