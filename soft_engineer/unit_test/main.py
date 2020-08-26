import requests
import unittest
import pytest

from mock import patch
from types import SimpleNamespace

r_req = SimpleNamespace(status_code=100)


def function():
    r =requests.get('https://xkcd.com/1906/')
    return r.status_code


# O lambda com args dentro do metodo, ja passa os parametros necessarios
# para o metodo a ser mocado e adiciona o retorno
@patch("main.requests.get", lambda *_, **__: r_req)
def test_function_error():
    a = function()
    assert a == 200 # print(a)

def test_function_ok():
    a = function()
    assert a == 200 # print(a)