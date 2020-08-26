import airflow
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.bash_operator import BashOperator


default_args = {
    'start_date': datetime(2019, 10, 14, 3, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past': False,
}

dag = DAG(
    dag_id='docker_example_local',
    default_args=default_args,
    schedule_interval='@hour',
)


t2 = DockerOperator(
    task_id='primeira_maquina',
    image='id_aws.dkr.ecr.us-east-1.amazonaws.com/nome-imagem-docker:latest',
    command='python3 main.py',
    api_version='auto',
    force_pull=True,
    auto_remove=True,
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',

    dag=dag
)

t3 = DockerOperator(
    task_id='segunda_maquina',
    image='id_aws.dkr.ecr.us-east-1.amazonaws.com/nome-imagem-docker:latest',
    command='python3 main.py',
    api_version='auto',
    force_pull=True,
    auto_remove=True,
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',

    dag=dag
)

t4 = BashOperator(
    task_id='limpando_as_maquinas',
    bash_command='docker container prune',
    dag=dag
)

t2 >> t3 >> t4