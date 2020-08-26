import airflow
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.bash_operator import BashOperator


from airflow.hooks.base_hook import BaseHook


default_args = {
    'start_date': datetime(2019, 10, 14, 3, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past': False,
}

dag = DAG(
    dag_id='docker_example_aws',
    default_args=default_args,
    schedule_interval='@daily',
)

t1 = BashOperator(
    task_id='ecr_login',
    bash_command='$(aws ecr get-login --region us-east-1 --no-include-email)',
    env={
        'AWS_ACCESS_KEY_ID':BaseHook.get_connection('aws_prod').login,
        'AWS_SECRET_ACCESS_KEY':BaseHook.get_connection('aws_prod').password
    },
    dag=dag
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
    environment={
        'AWS_ACCESS_KEY_ID':BaseHook.get_connection('aws_prod').login,
        'AWS_SECRET_ACCESS_KEY':BaseHook.get_connection('aws_prod').password
    },
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
    environment={
        'AWS_ACCESS_KEY_ID':BaseHook.get_connection('aws_prod').login,
        'AWS_SECRET_ACCESS_KEY':BaseHook.get_connection('aws_prod').password
    },
    dag=dag
)

t4 = BashOperator(
    task_id='limpando_as_maquinas',
    bash_command='docker container prune',
    dag=dag
)

t1 >> t2 >> t3 >> t4