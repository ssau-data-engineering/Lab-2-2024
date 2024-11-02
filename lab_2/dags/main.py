from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator  # Добавляем импорт
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount 
from airflow.models import Variable

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
    poke_interval=10,
    filepath='/opt/airflow/data/videos',
    fs_conn_id='vas_lab',
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='jrottenberg/ffmpeg',
    command='-i /data/videos/final.mp4 -vn /data/audios/audio.wav',
    mounts=[Mount(source='/data/videos', target='/data/videos', type='bind'),
            Mount(source='/data/audios', target='/data/audios', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    auto_remove=True,
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='vasser232/whisper',
    command='--input_file /data/input/audio.wav --output_file /data/output/transcript.txt --max_length 80',
    mounts=[Mount(source='/data/audios', target='/data/input', type='bind'),
            Mount(source='/data/texts', target='/data/output', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    auto_remove=True,
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='vasser232/text-summarizer',
    command='--input_file /data/input/transcript.txt --output_file /data/output/summary.txt --max_length 1000 --min_length 500',
    mounts=[Mount(source='/data/texts', target='/data/input', type='bind'),
            Mount(source='/data/texts', target='/data/output', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    auto_remove=True,
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='vasser232/save-to-pdf',
    command=[
        "python", "/data/txt_to_pdf.py", 
        "--general_file", "/data/input/transcript.txt",
        "--conspect_file", "/data/input/summary.txt",
        "--out_pdf_file", "/data/output/result.pdf"
    ],
    mounts=[
        Mount(source='/data/texts', target='/data/input', type='bind'),
        Mount(source='/data/texts', target='/data/output', type='bind')
    ],
    docker_url="tcp://docker-proxy:2375",
    auto_remove=True,
    dag=dag,
)





wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf