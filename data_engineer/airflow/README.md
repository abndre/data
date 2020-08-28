# AIRFLOW

Aqui exemplos de projetos utilizando o [Apache Airflow](https://airflow.apache.org)

# Como instalar:

Recomendo usar a versao 3.6 do python, devido a problemas de versoes.

````python
# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
export AIRFLOW_HOME=~/airflow

virtualenv -p python3.6 env

sourve env/bin/activate

# install from pypi using pip
pip install apache-airflow

# initialize the database
airflow initdb

# start the web server, default port is 8080
airflow webserver -p 8080

# start the scheduler
airflow scheduler

# visit localhost:8080 in the browser and enable the example dag in the home page
````

