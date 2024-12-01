import os
import datetime
from docker.types import Mount
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor


def get_input():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data/input_video.mp4')


dag = DAG(
    'second_lab',
    dagrun_timeout=datetime.timedelta(minutes=60),
    start_date=datetime.datetime(2024, 1, 1),
    description='DAG for extracting audio, transforming to text, summarizing, and saving as PDF',
    schedule_interval=None,
)

wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10,
    filepath = get_input(),
    fs_conn_id='second_lab_con',
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='cordanius/second_lab:first_pipeline', 
    command='ffmpeg -y -i /data/input_video.mp4 -vn /data/audio.mp3',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='cordanius/second_lab:first_pipeline',
    command='python audio_to_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='cordanius/second_lab:first_pipeline',
    command='python summarize_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='cordanius/second_lab:first_pipeline',
    command='python save_to_pdf.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf