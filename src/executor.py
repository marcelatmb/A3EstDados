# executor.py
# ============================================================
# Loop principal: lê expressão, faz parse, coleta variáveis,
# pede valores, avalia AST e imprime árvore (LISP e visual).
# ============================================================

from parser import Parser, NumberNode, VariableNode, UnaryOpNode, BinaryOpNode
from complexos import Complexo, ErroMatematico
from arvore import lisp, arvore

# ------------------ utilitário: parse de entrada complexa ------------------
def parse_complex_input(s: str) -> Complexo:
    """Converte texto do usuário para Complexo.
    Formatos aceitos: 'a+bi', 'a-bi', 'bi', 'a', '+i', '-i', '3.2+4.1i', etc.
    """
    s = s.strip().replace(" ", "")
    if s == "":
        raise ValueError("Entrada vazia")

    # lidar com i stand-alone
    s = s.replace("I", "i")
    if "i" in s:
        s_no_i = s[:-1] if s.endswith("i") else s  # remove 'i' final quando presente
        # se acabou vazio -> 'i' => 1i
        if s_no_i == "" or s_no_i == "+":
            return Complexo(0.0, 1.0)
        if s_no_i == "-":
            return Complexo(0.0, -1.0)
        # encontrar separador entre real/imag (scan a partir do segundo caractere)
        sep = None
        for i, ch in enumerate(s_no_i[1:], start=1):
            if ch in "+-":
                sep = i
                break
        if sep is None:
            # apenas parte imaginária, ex: '4i' ou '-4i'
            imag = float(s_no_i)
            return Complexo(0.0, imag)
        else:
            real_part = s_no_i[:sep]
            imag_part = s_no_i[sep:]
            real = float(real_part) if real_part not in ("", "+", "-") else (0.0 if real_part == "" else float(real_part))
            imag = float(imag_part)
            return Complexo(real, imag)
    else:
        # apenas real
        return Complexo(float(s), 0.0)

# ------------------ coletar variáveis ------------------
def coletar_variaveis(node, conjunto):
    """Popula 'conjunto' com nomes de variáveis presentes na AST."""
    if node is None:
        return
    if isinstance(node, VariableNode):
        conjunto.add(node.name)
    elif isinstance(node, UnaryOpNode):
        coletar_variaveis(node.child, conjunto)
    elif isinstance(node, BinaryOpNode):
        coletar_variaveis(node.left, conjunto)
        coletar_variaveis(node.right, conjunto)
    # NumberNode -> nada

# ------------------ avaliador ------------------
def eval_node(node, vars_dict):
    """Avalia a AST recursivamente retornando Complexo ou bool (para '=')"""
    if isinstance(node, NumberNode):
        return node.value
    if isinstance(node, VariableNode):
        if node.name not in vars_dict:
            raise NameError(f"Valor para variável '{node.name}' não fornecido")
        return vars_dict[node.name]
    if isinstance(node, UnaryOpNode):
        val = eval_node(node.child, vars_dict)
        if node.op in ("u+", "+"):
            return val
        if node.op in ("u-", "-"):
            return Complexo(-val.a, -val.b)
        if node.op == "conj":
            return val.conjugado()
        raise ValueError(f"Operador unário desconhecido: {node.op}")
    if isinstance(node, BinaryOpNode):
        left = eval_node(node.left, vars_dict)
        right = eval_node(node.right, vars_dict)
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
            # otimização: expoente inteiro real
            if right.b == 0 and float(right.a).is_integer():
                return left ** int(right.a)
            return left ** right
        if op == "raiz":
            # raiz(base, ordem) -> base ** (1/ordem)
            one = Complexo(1.0, 0.0)
            return left ** (one / right)
        if op == "=":
            return left == right
        raise ValueError(f"Operador binário desconhecido: {op}")
    raise TypeError("Nó AST desconhecido")

# ------------------ loop principal ------------------
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
                # parse
                ast = p.parse(expr)

                # imprimir LISP
                print("\nÁrvore (LISP):")
                print(lisp(ast))

                # imprimir visual
                print("\nÁrvore (visual):")
                arvore(ast)

                # coletar e pedir valores das variáveis (se houver)
                vars_set = set()
                coletar_variaveis(ast, vars_set)
                vars_dict = {}
                for var in sorted(vars_set):
                    while True:
                        entrada = input(f"Valor para {var} (formato a+bi): ").strip()
                        try:
                            vars_dict[var] = parse_complex_input(entrada)
                            break
                        except Exception as e:
                            print("Entrada inválida:", e)

                # avaliar
                res = eval_node(ast, vars_dict)
                print("\nResultado:")
                print(res)
            except ErroMatematico as em:
                print("Erro:", em)
            except Exception as e:
                print("Erro:", e)
    except KeyboardInterrupt:
        print("\nEncerrando.")
