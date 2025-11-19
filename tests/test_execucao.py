from src.executor import Executor
from src.parser import Parser


def executar(expr):
    arv = Parser(expr).parse()
    return Executor().executar(arv)


def test_execucao_soma_simples():
    assert executar("3+4").real == 7
    assert executar("3+4").imag == 0


def test_execucao_operacao_composta():
    resultado = executar("2*(3+4)")
    assert resultado.real == 14
    assert resultado.imag == 0


def test_execucao_com_complexos():
    resultado = executar("(2+3i) + (1+1i)")
    assert resultado.real == 3
    assert resultado.imag == 4


def test_execucao_divisao_por_zero():
    try:
        executar("3 / (0)")
    except Exception:
        assert True
    else:
        assert False
