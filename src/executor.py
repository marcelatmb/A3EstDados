import re
from parser import Parser, NumberNode, UnaryOpNode, BinaryOpNode
from complexos import Complexo
from erros import ErroMatematico
from arvore import lisp, arvore

# =======================================================
# Função de Pré-processamento para Raiz n-ésima
# =======================================================

def pre_process_expr(expr):
    """Converte a sintaxe raiz(base, ordem) para potenciação (base**(1/ordem))."""
    # Regex que encontra 'raiz(ARG1, ARG2)'
    # ([^,]+?) e ([^)]+?) capturam a base e a ordem de forma não-gananciosa.
    pattern = r"raiz\s*\(([^,]+?)\s*,\s*([^)]+?)\)" 
    
    def replacement(match):
        base = match.group(1).strip()
        n = match.group(2).strip()
        # Converte para a sintaxe de potenciação que o parser entende
        return f"({base}**(1.0/{n}))" 
    
    # Loop para substituir todas as ocorrências de raiz(...) (útil para raízes aninhadas)
    count = 1
    while count > 0:
        expr, count = re.subn(pattern, replacement, expr)
        
    return expr

def eval_node(node):
    """Avalia a AST recursivamente e retorna Complexo."""
    if isinstance(node, NumberNode):
        return node.value

    if isinstance(node, UnaryOpNode):
        val = eval_node(node.child)
        if node.op == "conj":
            return val.conjugado()
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
                # 1. Pré-processar a expressão para converter raiz(a, b) para potenciação
                processed_expr = pre_process_expr(expr)
                
                # 2. Fazer o parsing da expressão processada
                ast = p.parse(processed_expr)
                
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