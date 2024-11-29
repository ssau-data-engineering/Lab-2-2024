from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor

from docker.types import Mount

from utils.api_keys_hub import FS_CONN_ID, DOCKER_URL

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'audio_to_text_to_summary_to_pdf',
    default_args=default_args,
    description='DAG for extracting audio, transforming to text, summarizing, and saving as PDF',
    schedule_interval=None,
)

wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10,  # Interval to check for new files (in seconds)
    filepath='./data/input_data',  # Target folder to monitor
    fs_conn_id=FS_CONN_ID, # Check FAQ for info //
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='jrottenberg/ffmpeg:4.4-alpine',
    command='-i /data/input_data/input_video.mp4 -vn -y /data/prepared_data/audio.wav',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url=DOCKER_URL,
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='nyurik/alpine-python3-requests',
    command='python /data/transfrom_audio_to_text.py --input /data/prepared_data/audio.wav --output /data/prepared_data/text.txt',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url=DOCKER_URL,
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='nyurik/alpine-python3-requests',
    command='python /data/summarize_text.py --input /data/prepared_data/text.txt --output /data/prepared_data/summary.txt',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url=DOCKER_URL,
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='bikc/report:1.1',
    command='python /data/save_to_pdf.py --input /data/prepared_data/summary.txt --output /data/output_data/result.pdf',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url=DOCKER_URL,
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf