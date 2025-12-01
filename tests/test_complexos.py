import pytest
from src.complexos import Complexo, ErroMatematico


def test_criacao_basica():
    c = Complexo(2, 3)
    assert c.a == 2
    assert c.b == 3


def test_soma():
    a = Complexo(2, 3)
    b = Complexo(1, 4)
    r = a + b
    assert r == Complexo(3, 7)


def test_subtracao():
    a = Complexo(5, -2)
    b = Complexo(1, 4)
    r = a - b
    assert r == Complexo(4, -6)


def test_multiplicacao():
    a = Complexo(2, 3)
    b = Complexo(1, 1)
    r = a * b
    assert r == Complexo(-1, 5)


def test_divisao():
    a = Complexo(3, 2)
    b = Complexo(1, -1)
    r = a / b
    assert r == Complexo(0.5, 2.5)


def test_divisao_por_zero():
    a = Complexo(3, 2)
    b = Complexo(0, 0)
    with pytest.raises(ErroMatematico):
        _ = a / b


def test_conjugado():
    a = Complexo(3, -4)
    r = a.conjugado()
    assert r == Complexo(3, 4)


def test_potencia():
    a = Complexo(2, 1)
    r = a ** 2
    assert r == Complexo(3, 4)


def test_igualdade():
    a = Complexo(2, 3)
    b = Complexo(2, 3)
    assert a == b