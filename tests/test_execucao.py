from src.executor import Executor, eval_node, coletar_variaveis
from src.parser import Parser
from src.complexos import Complexo, ErroMatematico


def executar(expr, vars_dict=None):
    if vars_dict is None:
        vars_dict = {}
    arv = Parser().parse(expr)
    return eval_node(arv, vars_dict)


def test_execucao_soma_simples():
    resultado = executar("3+4")
    assert resultado == Complexo(7, 0)


def test_execucao_operacao_composta():
    resultado = executar("2*(3+4)")
    assert resultado == Complexo(14, 0)


def test_execucao_com_complexos():
    resultado = executar("(2+3i) + (1+1i)")
    assert resultado == Complexo(3, 4)


def test_execucao_divisao_por_zero():
    with pytest.raises(ErroMatematico):
        executar("3 / 0")


def test_execucao_com_variaveis():
    resultado = executar("x + y", {"x": Complexo(2, 1), "y": Complexo(3, 2)})
    assert resultado == Complexo(5, 3)


def test_execucao_potencia():
    resultado = executar("2**3")
    assert resultado == Complexo(8, 0)