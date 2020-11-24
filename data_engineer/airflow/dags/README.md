# Dags

As Dags sao onde podemos construir nossos pipelines, com elas facilitamos em muito o processo de
ETL ou ELT

# Dag Docker

Para usar atualmente o docker operator, recomendo usar o python3.6 e e necessario instalar
o docker do python

[DAG DOCKER AWS](dag_docker_aws.py)

Esta exemplo de dag, possui as imagens salvas na [ECR](https://aws.amazon.com/pt/ecr/), e dentro de nossa instancia do airflow estamos rodando a imagem docker

[DAG DOCKER](dag_docker_local.py)


Este exemplo pode ser utilizado para criar um workflow dinamico para o airflow.

[DAG DINÂMICA](dag_auto_workflow.py)

# Requisitos docker no airflow
Para utilizar o docker dentro do airflow, se faz necessario instalar:

````python
pip install docker
````
