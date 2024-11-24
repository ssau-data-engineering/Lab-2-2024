from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'retries': 1,
}

TOKEN = Variable.get('API_TOKEN_HG')

dag = DAG(
    dag_id='LAB2_TASK1',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(1),
)

# 1. Мониторинг папки
file_sensor_task = FileSensor(
    task_id='monitor_folder',
    poke_interval=10,
    timeout=600,
    filepath='./data/videos/new_video.mp4',  # Конкретный файл
    fs_conn_id='lab2_task1',
    dag=dag,
)

# 2. Извлечение аудио из видео
extract_audio_task = DockerOperator(
    task_id='extract_audio',
    image='jrottenberg/ffmpeg:4.4-alpine',
    command="-i /data/videos/new_video.mp4 -vn /data/audio/extracted_audio.wav",
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

# 3. Преобразование аудио в текст
convert_audio_to_text_task = DockerOperator(
    task_id='convert_audio_to_text',
    image='nyurik/alpine-python3-requests',
    command=f"python /data/audio_to_text.py --token {TOKEN}",
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

# 4. Составление конспекта

summarize_text_task = DockerOperator(
    task_id='summarize_text',
    image='nyurik/alpine-python3-requests',
    command=f'python /data/summarize_text.py --token {TOKEN}',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

# 5. Генерация PDF
generate_pdf_task = DockerOperator(
    task_id='generate_pdf',
    image='rusekk/fpdf-python',
    command=f'python /data/to_pdf.py',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

file_sensor_task >> extract_audio_task >> convert_audio_to_text_task >> summarize_text_task >> generate_pdf_task