from src.parser import Parser
from src.executor import eval_node
from src.complexos import Complexo, ErroMatematico


def test_erro_sintaxe_simples():
    with pytest.raises(SyntaxError):
        Parser().parse("3+*4")


def test_erro_token_invalido():
    with pytest.raises(SyntaxError):
        Parser().parse("2 # 3")


def test_erro_divisao_zero():
    arvore = Parser().parse("3 / 0")
    with pytest.raises(ErroMatematico):
        eval_node(arvore, {})


def test_erro_variavel_indefinida():
    arvore = Parser().parse("x + 5")
    with pytest.raises(NameError):
        eval_node(arvore, {})