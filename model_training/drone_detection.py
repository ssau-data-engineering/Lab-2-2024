from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor

from docker.types import Mount
import docker.types

from utils.api_keys_hub import FS_CONN_ID, DOCKER_URL

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'drone_detection',
    default_args=default_args,
    description='Detecting drones and some other objects on image',
    schedule_interval=None,
)

wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10,  # Interval to check for new files (in seconds)
    filepath='./data/input_data',  # Target folder to monitor
    fs_conn_id=FS_CONN_ID, # Check FAQ for info //
    dag=dag,
)

transform_raw_data_to_dataset = DockerOperator(
    task_id='transform_raw_data_to_dataset',
    image='fvt34u/python-pillow',
    command='/data/make_dataset.py --input /data/input_data/synth_drone_data.zip --output /data/prepared_data/synth_drone \
        --data_type synth --input_data_as_zip --use_translate_to_yolo',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url=DOCKER_URL,
    dag=dag,
)

yolo_training = DockerOperator(
    task_id='yolo_training',
    image='ultralytics/ultralytics',
    command='python /data/train_yolo.py --input /data/prepared_data/synth_drone --output /data/output_data/yolo',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url=DOCKER_URL,
    device_requests=[
        docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])
    ],
    dag=dag,
)

wait_for_new_file >> transform_raw_data_to_dataset >> yolo_training