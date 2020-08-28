# Criando um docker container com um projeto python

Basicamente tem-se a seguinte estrutura:

````
Dockerfile
dev/
requeriments.txt
````

A estrutura do [Dockerfile](Dockerfile). Ele copia a pasta dev para dentro do container, instala os  [requirements](requirements.txt) e executa os script [main](/docker/dev/main.py) ao ser iniciado. Onde toda a logica fica dentro dele.

Para executar:

````
docker build -t nomedaimagem .
````

O legal desta imagem que temos duas variaveis de ambiente, que podemos passar quando formos
executar o container:

````
docker run -it --rm -name nomedopod -e V1=1 -e V2=2 nomedaimagem
````

e no seu codigo python so adicionar:

````python
import os

V1 = os.environ['V1']
````

Caso utilize o airflow+docker, podera ainda adicionar a variavel de ambiente no seguinte formato:

````python
DockerOperator(
    task_id='tas_id',
    image='nomedaimagem:latest',
    command='python main.py',
    api_version='auto',
    auto_remove=True,
    force_pull=True,
    docker_url='unix://var/run/docker.sock',
    network_mode='bridge',
    environment={
        'V1':'algo',
        'V2':'novo'
    },
    dag=dag
)
````
