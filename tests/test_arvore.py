from src.arvore import No


def test_no_simples():
    n = No("3")
    assert n.valor == "3"
    assert n.esquerda is None
    assert n.direita is None


def test_no_com_filhos():
    n = No("+", No("2"), No("3"))
    assert n.valor == "+"
    assert n.esquerda.valor == "2"
    assert n.direita.valor == "3"


def test_impressao_lisp_soma():
    n = No("+", No("3"), No("4"))
    assert n.to_lisp() == "(+ 3 4)"


def test_impressao_lisp_expressao_aninhada():
    n = No("*", No("+", No("3"), No("4")), No("5"))
    assert n.to_lisp() == "(* (+ 3 4) 5)"
