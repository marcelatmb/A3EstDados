import pytest
from src.erros import ErroSintaxe, ErroMatematico
from src.parser import Parser
from src.executor import Executor


def test_erro_sintaxe_simples():
    with pytest.raises(ErroSintaxe):
        Parser("3+*4").parse()


def test_erro_token_invalido():
    with pytest.raises(ErroSintaxe):
        Parser("2 # 3").parse()


def test_erro_divisao_zero():
    arvore = Parser("3 / 0").parse()
    with pytest.raises(ErroMatematico):
        Executor().executar(arvore)
