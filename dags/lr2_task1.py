import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount


dag = DAG(
    dag_id="LR_2_task_1",
    schedule="0 0 * * *", 
    start_date=datetime.datetime(2024, 11, 1, tzinfo=datetime.timezone.utc), 
    catchup=False,  
    dagrun_timeout=datetime.timedelta(minutes=60),  
    tags=["LR"],
)

wait_for_new_file = FileSensor(
    task_id='wait_for_new_file',
    poke_interval=10, 
    filepath='./data/LR_2_task1/WC.mp4',  
    fs_conn_id='file-connection-id', 
    dag=dag,
)

extract_audio = DockerOperator(
    task_id='extract_audio',
    image='gr0mozeka/ffmpeg_imag:1.0',
    command='ffmpeg -i /data/LR_2_task1/WC.mp4 -vn /data/LR_2_task1/audio.wav',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

transform_audio_to_text = DockerOperator(
    task_id='transform_audio_to_text',
    image='gr0mozeka/ml_model_image:1.0',
    command='python /data/LR_2_task1/audio_to_text.py --input audio.wav --output text.txt',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

summarize_text = DockerOperator(
    task_id='summarize_text',
    image='gr0mozeka/ml_model_image:1.0',
    command='python /data/LR_2_task1/summarize_text.py --input text.txt --output summary.txt',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

save_to_pdf = DockerOperator(
    task_id='save_to_pdf',
    image='gr0mozeka/to_pdf:1.0',
    command='python /data/LR_2_task1/save_to_pdf.py --input summary.txt --output result.pdf',
    mounts=[Mount(source='/data', target='/data', type='bind')],
    docker_url="tcp://docker-proxy:2375",
    dag=dag,
)

wait_for_new_file >> extract_audio >> transform_audio_to_text >> summarize_text >> save_to_pdf