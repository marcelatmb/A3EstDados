from src.arvore import no


def test_no_simples():
    n = no("3")
    assert n.valor == "3"
    assert n.esquerda is None
    assert n.direita is None


def test_no_com_filhos():
    n = no("+", no("2"), no("3"))
    assert n.valor == "+"
    assert n.esquerda.valor == "2"
    assert n.direita.valor == "3"


def test_impressao_lisp_soma():
    n = no("+", no("3"), no("4"))
    assert n.to_lisp() == "(+ 3 4)"


def test_impressao_lisp_expressao_aninhada():
    n = no("*", no("+", no("3"), no("4")), no("5"))
    assert n.to_lisp() == "(* (+ 3 4) 5)"
