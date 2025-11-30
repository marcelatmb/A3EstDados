# arvore.py
# ============================================================
# Impressão da AST em notação LISP e impressão visual
# Compatível com nós: NumberNode, VariableNode, UnaryOpNode, BinaryOpNode
# ============================================================

from parser import NumberNode, VariableNode, UnaryOpNode, BinaryOpNode

# ------------------ lisp (notação) ------------------
def lisp(no):
    """Retorna string em notação LISP para a subárvore `no`."""
    if no is None:
        return ""
    # número
    if isinstance(no, NumberNode):
        return str(no.value)
    # variável
    if isinstance(no, VariableNode):
        return str(no.name)
    # unário
    if isinstance(no, UnaryOpNode):
        return f"({no.op} {lisp(no.child)})"
    # binário
    if isinstance(no, BinaryOpNode):
        return f"({no.op} {lisp(no.left)} {lisp(no.right)})"
    return "?"

# ------------------ arvore (visual) ------------------
def arvore(no, prefix=""):
    """Imprime a árvore em formato visual legível."""
    if no is None:
        return
    # mostrar o próprio nó
    if isinstance(no, NumberNode):
        print(prefix + f"└── Number: {no.value}")
        return
    if isinstance(no, VariableNode):
        print(prefix + f"└── Variable: {no.name}")
        return
    if isinstance(no, UnaryOpNode):
        print(prefix + f"└── UnaryOp: {no.op}")
        arvore(no.child, prefix + "    ")
        return
    if isinstance(no, BinaryOpNode):
        print(prefix + f"└── BinaryOp: {no.op}")
        arvore(no.left, prefix + "    ")
        arvore(no.right, prefix + "    ")
        return
    print(prefix + "└── ?")
