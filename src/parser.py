import re
from complexos import Complexo

# ---------------------------------------------------------
# NODES
# ---------------------------------------------------------

class Node: pass

class NumberNode(Node):
    def __init__(self, value):
        self.value = value   # instância de Complexo
    def __repr__(self):
        return f"Number({repr(self.value)})"

class VariableNode(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Variable({self.name})"

class BinaryOpNode(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.op} {self.left} {self.right})"

class UnaryOpNode(Node):
    def __init__(self, op, child):
        self.op = op
        self.child = child
    def __repr__(self):
        return f"({self.op} {self.child})"


class FunctionNode(Node):
    """Para funções estilo: raiz(expr), conj(expr), etc."""
    def __init__(self, func_name, child):
        self.func_name = func_name
        self.child = child
    def __repr__(self):
        return f"{self.func_name}({self.child})"


# ---------------------------------------------------------
# PARSER
# ---------------------------------------------------------

class Parser:
    def __init__(self):
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "**": 4
        }

        # Funções unárias chamadas por nome
        self.functions = {"conj", "raiz"}

    def tokenize(self, expr):
        expr = expr.replace(" ", "")

        token_pattern = r"""
            (\*\*)                    |  # potência
            ([A-Za-z_]\w*)            |  # variáveis ou funções
            ([+-]?\d+\.\d+[+-]\d+\.\d+i) | 
            ([+-]?\d+\.\d+[+-]\d+i)      |
            ([+-]?\d+[+-]\d+\.\d+i)      |
            ([+-]?\d+[+-]\d+i)           |  # a+bi
            ([+-]?\d+\.\d+i)             |  # 2.5i
            ([+-]?\d+i)                  |  # 2i
            ([+-]?\d+\.\d+)              |  # reais decimais
            ([+-]?\d+)                   |  # inteiros
            (\() | (\))                  |  # parênteses
            (\+)|(\-)|(\*)|(\/)             # operadores
        """

        raw = re.finditer(token_pattern, expr, re.VERBOSE)
        tokens = [m.group(0) for m in raw]

        if "".join(tokens) != expr:
            raise ValueError(f"Tokenização falhou em: {expr}. Tokens: {tokens}")

        return tokens

    # -----------------------------------------------------
    # PARSE PRINCIPAL (Shunting Yard)
    # -----------------------------------------------------

    def parse(self, expr):
        tokens = self.tokenize(expr)
        output = []
        ops = []

        def aplicar():
            op = ops.pop()

            # Função unária
            if op in self.functions:
                child = output.pop()
                output.append(FunctionNode(op, child))
                return

            # Operador unário de sinal
            if op in ("+", "-") and (not output or isinstance(output[-1], str)):
                child = output.pop()
                output.append(UnaryOpNode(op, child))
                return

            # Operador binário
            right = output.pop()
            left = output.pop()
            output.append(BinaryOpNode(op, left, right))

        i = 0
        while i < len(tokens):
            t = tokens[i]

            # ----------------------------
            # LITERAIS COMPLEXOS OU NÚMEROS
            # ----------------------------
            if self.is_complex_literal(t):
                real, imag = self.parse_complex_literal(t)
                output.append(NumberNode(Complexo(real, imag)))

            # ----------------------------
            # VARIÁVEIS OU FUNÇÕES
            # ----------------------------
            elif re.match(r"^[A-Za-z_]\w*$", t):
                if t in self.functions:
                    ops.append(t)
                else:
                    output.append(VariableNode(t))

            # ----------------------------
            # PARÊNTESES
            # ----------------------------
            elif t == "(":
                ops.append("(")

            elif t == ")":
                while ops and ops[-1] != "(":
                    aplicar()
                if not ops:
                    raise ValueError("Parênteses desbalanceados")
                ops.pop()  # remove "("

                # Se houver função pendente: raiz (...) ou conj (...)
                if ops and ops[-1] in self.functions:
                    aplicar()

            # ----------------------------
            # OPERADORES
            # ----------------------------
            elif t in self.precedence:
                # Checa se operador é unário
                is_unary = (t in ("+", "-")) and (
                    i == 0 or tokens[i-1] in self.precedence or tokens[i-1] == "("
                )
                if is_unary:
                    ops.append(t)
                else:
                    # Binário: respeita precedência
                    while (ops and ops[-1] in self.precedence and
                           ((self.precedence[ops[-1]] > self.precedence[t]) or
                            (self.precedence[ops[-1]] == self.precedence[t] and t != "**"))):
                        aplicar()
                    ops.append(t)

            else:
                raise ValueError(f"Token inesperado: {t}")

            i += 1

        # ----------------------------
        # FINAL: limpa pilha de operadores
        # ----------------------------
        while ops:
            if ops[-1] == "(":
                raise ValueError("Parênteses desbalanceados ao final")
            aplicar()

        return output[-1]

    # ---------------------------------------------------------
    # Funções auxiliares
    # ---------------------------------------------------------

    def is_complex_literal(self, s):
        return bool(re.match(
            r"^[+-]?\d+(\.\d+)?[+-]\d+(\.\d+)?i$|^[+-]?\d+(\.\d+)?i$|^[+-]?i$|^[+-]?\d+(\.\d+)?$",
            s
        ))

    def parse_complex_literal(self, s: str):
        s = s.strip().replace(" ", "")
        if "i" not in s:
            return float(s), 0.0
        if s in ("i", "+i"):
            return 0.0, 1.0
        if s == "-i":
            return 0.0, -1.0

        m = re.match(r"^([+-]?\d+(\.\d+)?)([+-]\d+(\.\d+)?)i$", s)
        if m:
            return float(m.group(1)), float(m.group(3))

        m2 = re.match(r"^([+-]?\d+(\.\d+)?)i$", s)
        if m2:
            return 0.0, float(m2.group(1))

        raise ValueError(f"Literal complexo inválido: {s}")