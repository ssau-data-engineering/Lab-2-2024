import os
from datetime import datetime
from airflow import DAG
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 18),
    'retries': 1,
}

dag = DAG(
    'video_to_audio_to_text',
    default_args=default_args,
    description='Extract audio from video and convert it to text in PDF format',
    schedule_interval=None,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_input = os.path.join(current_dir, '..', 'data')

wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10,
    filepath=path_to_input,
    fs_conn_id='lab_connect',
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='dekartvon/ffmpeg-image',
    command='ffmpeg -i /data/input.mp4 -vn /data/audio.wav',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='dekartvon/requests-image',
    command='python /data/audio_to_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='dekartvon/requests-image',
    command='python /data/summarize_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='dekartvon/fpdf-image',
    command='python /data/save_to_pdf.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf