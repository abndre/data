from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator


def start(*args, **kwargs):
    print("START")


def print_values():
    print("Teste")


def end(*args, **kwargs):
    print("END DAGS")


default_args = {
    'start_date': datetime(2020, 11, 19, 23, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
    'depends_on_past': False,
}

dag = DAG(
    dag_id='teste_dynamic_workflow',
    default_args=default_args,
    schedule_interval='*/3 * * * *',
    catchup=False
)


starting_task = PythonOperator(
    task_id='start',
    dag=dag,
    provide_context=True,
    python_callable=start,
    op_args=[])

ending_task = PythonOperator(
    task_id='end',
    dag=dag,
    provide_context=True,
    python_callable=end,
    op_args=[])


def doSomeWork(name, index, *args, **kwargs):
    # Do whatever work you need to do
    # Here I will just create a new file
    # time.sleep(int(index) * 5)
    print(f"{name} - {index}")


list_queries = ['work1', 'work2', 'work3']

for querie in list_queries:
    dynamicTask = PythonOperator(
        task_id='docker_integrador_salesforce_consulta_{}'.format(querie),
        dag=dag,
        provide_context=True,
        python_callable=doSomeWork,
        op_args=['querie', querie])

    starting_task.set_downstream(dynamicTask)
    dynamicTask.set_downstream(ending_task)

