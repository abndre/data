# Organizacao testes

Para deixar o teste mais organizado, pode-se utilizar a estrutura

````
├── app
│   ├── __init__.py # make it a package
│   └── main.py
└── tests
    ├── __init__.py # make it a package
    └── test_main.py
````

Para testar execute dentro da pasta *app*

````
pytest
````

Cobertura de testes

````
coverage run -m pytest
coverage html --omit="*usr/*"
````

Este omit auxilia a remocao de validacoes desnecessarias, ou fora do projeto *app*.