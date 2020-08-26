# Testando com Mock

Para tornar o codigo totalmente coberto, e dentro da ideia de testes de unidade,
utiliza-se o mock em algumas funcoes


````python
import requests

def function():
    r =requests.get('https://xkcd.com/1906/')
    return (r.status_code)
````

Para testar a funcao, o mock.patch auxilia a nao fazer a request para fora do contexto.

`````
execute no terminal
# pytest main.py 
`````