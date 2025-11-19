from parser import NumberNode, UnaryOpNode, BinaryOpNode

# ============================================================
#              Função que imprime em notação LISP
# ============================================================

def lisp(no):
    if no is None:
        return ""

    # Nó número
    if isinstance(no, NumberNode):
        return str(no.value)

    # Nó unário: (op child)
    if isinstance(no, UnaryOpNode):
        return f"({no.op} {lisp(no.child)})"

    # Nó binário: (op left right)
    if isinstance(no, BinaryOpNode):
        return f"({no.op} {lisp(no.left)} {lisp(no.right)})"

    # Qualquer coisa inesperada
    return "?"


# ============================================================
#              Função que imprime a árvore visual
# ============================================================

def arvore(no, grau=0):
    if no is None:
        return

    prefixo = "    " * grau

    # Nó número
    if isinstance(no, NumberNode):
        print(prefixo + f"---> {no.value}")
        return

    # Nó unário
    if isinstance(no, UnaryOpNode):
        print(prefixo + f"---> {no.op}")
        arvore(no.child, grau + 1)
        return

    # Nó binário
    if isinstance(no, BinaryOpNode):
        print(prefixo + f"---> {no.op}")
        arvore(no.left, grau + 1)
        arvore(no.right, grau + 1)
        return

    # fallback
    print(prefixo + "---> ?")
