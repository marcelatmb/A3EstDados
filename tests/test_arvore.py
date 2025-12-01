from src.parser import NumberNode, VariableNode, UnaryOpNode, BinaryOpNode
from src.arvore import lisp


def test_number_node():
    n = NumberNode(3)
    assert n.value == 3


def test_variable_node():
    n = VariableNode("x")
    assert n.name == "x"


def test_lisp_simple_number():
    n = NumberNode(3)
    assert lisp(n) == "3"


def test_lisp_simple_variable():
    n = VariableNode("x")
    assert lisp(n) == "x"


def test_lisp_unary_operation():
    n = UnaryOpNode("-", NumberNode(5))
    assert lisp(n) == "(- 5)"


def test_lisp_binary_operation():
    n = BinaryOpNode("+", NumberNode(3), NumberNode(4))
    assert lisp(n) == "(+ 3 4)"


def test_lisp_nested_expression():
    n = BinaryOpNode("*", BinaryOpNode("+", NumberNode(3), NumberNode(4)), NumberNode(5))
    assert lisp(n) == "(* (+ 3 4) 5)"