from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta, timezone
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from airflow.models import Variable


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 11, 30, tzinfo=timezone.utc), 
    'retries': 1,
}

api_token = Variable.get('API_TOKEN_HG')

dag = DAG(
    'audio_to_text_to_summary_to_pdf',
    default_args=default_args,
    description='DAG for extracting audio, transforming to text, summarizing, and saving as PDF',
    schedule_interval=None,
)

wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10,  
    filepath='./data/input_data/input_video.mp4', 
    fs_conn_id='file_conn',
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='jrottenberg/ffmpeg:4.4-alpine',
    command='-i /data/input_data/input_video.mp4 -vn  /data/audio.wav',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='nyurik/alpine-python3-requests',
    command= f'python /data/audio_to_text.py --token {api_token}',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='nyurik/alpine-python3-requests',
    command= f'python /data/summarize_text.py --token {api_token}',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='marelli0/my-fpdf-image:1.0',
    command='python /data/save_to_pdf.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)


wait_for_new_file >> extract_audio  >> transform_audio_to_text  >> summarize_text  >> save_to_pdf