from src.parser import Parser
from src.complexos import Complexo, ErroMatematico


def parse(expr):
    return Parser().parse(expr)


def test_parser_soma_simples():
    arv = parse("3+4")
    assert str(arv) == "BinaryOpNode(+, NumberNode(3.0), NumberNode(4.0))"


def test_parser_com_parênteses():
    arv = parse("2*(3+4)")
    # Verifica estrutura básica
    assert arv.op == "*"
    assert arv.left.value == Complexo(2, 0)


def test_precedencia_correta():
    arv = parse("2+3*4")
    # 3*4 deve ser avaliado primeiro
    assert arv.op == "+"
    assert arv.right.op == "*"


def test_parênteses_aninhados():
    arv = parse("((3+2)*4)")
    assert arv.op == "*"


def test_erro_sintaxe_duplo_operador():
    with pytest.raises(SyntaxError):
        parse("3++4")


def test_erro_sintaxe_parêntese_aberto():
    with pytest.raises(SyntaxError):
        parse("3+(")


def test_erro_sintaxe_token_invalido():
    with pytest.raises(SyntaxError):
        parse("3 + $ 4")