# Criando Dockercontainer

````
docker build --pull --rm -f "Dockerfile" -t scaladocker:latest "." <
````

# Rodar dockercontainer

````
docker run --rm -it  scaladocker:latest 
````