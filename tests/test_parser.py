import pytest
from src.parser import Parser
from src.erros import ErroSintaxe


def parse(expr):
    return Parser(expr).parse()


def test_parser_soma_simples():
    arv = parse("3+4")
    assert arv.to_lisp() == "(+ 3 4)"


def test_parser_com_parênteses():
    arv = parse("2*(3+4)")
    assert arv.to_lisp() == "(* 2 (+ 3 4))"


def test_precedencia_correta():
    arv = parse("2+3*4")
    assert arv.to_lisp() == "(+ 2 (* 3 4))"


def test_parênteses_aninhados():
    arv = parse("((3+2)*4)")
    assert arv.to_lisp() == "(* (+ 3 2) 4)"


def test_erro_sintaxe_duplo_operador():
    with pytest.raises(ErroSintaxe):
        parse("3++4")


def test_erro_sintaxe_parêntese_aberto():
    with pytest.raises(ErroSintaxe):
        parse("3+(")


def test_erro_sintaxe_token_invalido():
    with pytest.raises(ErroSintaxe):
        parse("3 + $ 4")
