# Dags

As Dags sao onde podemos construir nossos pipelines, com elas facilitamos em muito o processo de
ETL ou ELT

# Dag Docker

Para usar atualmente o docker operator, recomendo usar o python3.6 e e necessario instalar
o docker do python

[DAG DOCKER AWS](dag_docker_AWS.py)

Esta exemplo de dag, possui as imagens salvas na [ECR](https://aws.amazon.com/pt/ecr/), e dentro de nossa instancia do airflow estamos rodando a imagem docker

[DAG DOCKER](dag_docker_local.py)


````python
pip install docker
````
