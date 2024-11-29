from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount


default_args = {
    'owner': 'snail',
    'start_date': datetime(2024, 1, 1),
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
    filepath= '/opt/airflow/data',
    fs_conn_id='fs_default', # Target folder to monitor
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='jrottenberg/ffmpeg',
    command='-i /data/input_video.mp4 -vn -acodec copy /data/audio.aac',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    auto_remove = True,
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='snail911/ml_model_image',
    command='python /app/audio_to_text.py  /data/audio.aac  /data/text.txt',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)



summarize_text = DockerOperator(
    task_id='summarize_text',
    image='snail911/ml_model_image:v2',
    command='python /app/summarize_text.py  /data/text.txt  /data/summary.txt',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)


save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='snail911/ml_model_image:v3',
    command='python /app/save_to_pdf.py  /data/summary.txt  /data/result.pdf',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf
