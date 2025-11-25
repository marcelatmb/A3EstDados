import re
from parser import Parser, NumberNode, UnaryOpNode, BinaryOpNode
from complexos import Complexo, ErroMatematico
# Presumindo que 'arvore' e 'lisp' são importáveis
from arvore import lisp, arvore 

# Nota: Agora o parser já entende 'raiz' e 'conj', então pre_process_expr
# pode ser apenas identidade (mantive a função caso queira transformação extra)
def pre_process_expr(expr):
    return expr

def eval_node(node):
    """Avalia a AST recursivamente e retorna Complexo."""
    if isinstance(node, NumberNode):
        return node.value

    if isinstance(node, UnaryOpNode):
        val = eval_node(node.child)
        if node.op == "conj":
            return val.conjugado()
        if node.op in ("-", "u-"):
            return Complexo(-val.a, -val.b)
        if node.op in ("+", "u+"):
            return val
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
            # right é Complexo; se for inteiro real, usar int
            # A classe Complexo.__pow__ trata o tipo, então esta otimização é opcional
            if right.b == 0 and float(right.a).is_integer():
                return left ** int(right.a)
            return left ** right
        if op == "raiz":
            # raiz(base, ordem) => base ** (1 / ordem)
            # 1/ordem é tratado como Complexo
            denom = right
            # calcular 1/denom usando Complexo divisão
            one = Complexo(1.0, 0.0)
            return left ** (one / denom)
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
                # 1. Pré-processar (agora identidade)
                processed_expr = pre_process_expr(expr)

                # 2. Fazer o parsing da expressão processada
                ast = p.parse(processed_expr)

                print("\nÁrvore (LISP):")
                # A função lisp() precisa de tratamento de erro para AST incompleta/errada
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