from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount

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
    filepath='/opt/airflow/data/manch',  # Target folder to monitor
    fs_conn_id='manch_lab', # Check FAQ for info
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='jrottenberg/ffmpeg',
    command='-i /data/manch/final.mp4 -vn /data/aud/audio.wav',
    mounts=[Mount(source='/data/manch', target='/data/manch', type='bind'), 
            Mount(source='/data/aud', target='/data/aud', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='vmokook23/audio_text',
    command='--audio_file /data/aud/audio.wav --output_path /data/text/output.txt --width 80',
    mounts=[Mount(source='/data/aud', target='/data/aud', type='bind'), 
            Mount(source='/data/text', target='/data/text', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='vmokook23/text_conspect',
    command='--input_file /data/text/output.txt --output_file /data/summary/summary.txt',
    mounts=[Mount(source='/data/text', target='/data/text', type='bind'), 
            Mount(source='/data/summary', target='/data/summary', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='vmokook23/save_pdf',
    command='--input /data/summary/summary.txt --output /data/pdf/pdfka.pdf',
    mounts=[Mount(source='/data/summary', target='/data/summary', type='bind'),
            Mount(source='/data/pdf', target='/data/pdf', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf