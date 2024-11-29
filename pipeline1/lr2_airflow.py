import os
import datetime
from docker.types import Mount
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor


# Определение пути к данным
def get_input():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data/video.mp4')


dag = DAG(
    'audio_to_text_to_summary_to_pdf_1',
    dagrun_timeout=datetime.timedelta(minutes=45),
    start_date=datetime.datetime(2024, 1, 1),
    catchup=False,
    description='DAG for extracting audio, transforming to text, summarizing, and saving as PDF',
    schedule_interval=None,
)

wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10,  # Interval to check for new files (in seconds)
    filepath = get_input(), # Target folder to monitor
    fs_conn_id='airflow_lr2_connection', # Check FAQ for info
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='zse4vfr/image-lr2:1.4', 
    command='ffmpeg -y -i /data/video.mp4 -vn /data/audio.mp3',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='zse4vfr/image-lr2:1.4',
    command='python audio_to_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='zse4vfr/image-lr2:1.4',
    command='python summarize_text.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='zse4vfr/image-lr2:1.4',
    command='python save_to_pdf.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf