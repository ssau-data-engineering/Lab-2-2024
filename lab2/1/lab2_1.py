import os
import datetime
from airflow import DAG
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor

dag = DAG(
    'audio_to_text_to_summary_to_pdf',
    dagrun_timeout=datetime.timedelta(minutes=40),
    start_date=datetime.datetime(2024, 1, 1),
    catchup=False,
    description='DAG for extracting audio, transforming to text, summarizing, and saving as PDF',
    schedule_interval=None,
)

wait_for_new_file = FileSensor(
    task_id='wait_for_file',
    poke_interval=10,
    filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/input/input.mp4'),
    fs_conn_id='lab2-1',
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='irameis/dat-eng:ffmpeg',
    command='ffmpeg -y -i /data/input/input.mp4 -vn /data/audio.mp3',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='audio_2_text',
    image='irameis/dat-eng:requests-pdf',
    command='python /data/audio_2_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarization',
    image='irameis/dat-eng:requests-pdf',
    command='python /data/summarization.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_pdf',
    image='irameis/dat-eng:requests-pdf',
    command='python /data/save_pdf.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf