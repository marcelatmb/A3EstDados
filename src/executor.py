from parser import Parser, NumberNode, UnaryOpNode, BinaryOpNode
from complexos import Complexo, ErroMatematico
from arvore import lisp, arvore

def eval_node(node):
    """Avalia a AST recursivamente e retorna Complexo."""
    if isinstance(node, NumberNode):
        return node.value

    if isinstance(node, UnaryOpNode):
        val = eval_node(node.child)
        if node.op == "conj":
            return val.conjugado()
        if node.op == "raiz":
            # raiz padrão: raiz quadrada
            return val.raiz_n(2)
        if node.op == "-":
            return Complexo(-val.a, -val.b)
        raise ValueError(f"Operador unário desconhecido: {node.op}")

    if isinstance(node, BinaryOpNode):
        left = eval_node(node.left)
        right = eval_node(node.right)
        op = node.op
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            return left / right
        if op == "**":
            # right pode ser inteiro ou Complexo
            # converter right para Python float/int quando possível
            if right.b == 0 and float(right.a).is_integer():
                return left ** int(right.a)
            return left ** right
        raise ValueError(f"Operador binário desconhecido: {op}")

    raise TypeError("Nó AST desconhecido")

if __name__ == "__main__":
    p = Parser()
    try:
        while True:
            expr = input("Expressão > ").strip()
            if expr.lower() in ("sair", "exit", "quit"):
                break
            if not expr:
                continue
            try:
                ast = p.parse(expr)
                print("\nÁrvore (LISP):")
                print(lisp(ast))
                print("\nÁrvore (visual):")
                arvore(ast)
                print("\nResultado:")
                res = eval_node(ast)
                print(res)
            except Exception as e:
                print("Erro:", e)
    except KeyboardInterrupt:
        print("\nEncerrando.")
