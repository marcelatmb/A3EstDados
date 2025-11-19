import re
from complexos import Complexo


# ============================================================
#                DEFINIÇÃO DOS TIPOS DE NÓ DA AST
# ============================================================

class Node:
    pass


class NumberNode(Node):
    def __init__(self, value):
        self.value = value   # instância de Complexo
    def __repr__(self):
        return f"Number({self.value})"


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


# ============================================================
#                         PARSER
# ============================================================

class Parser:

    def __init__(self):
        # precedência dos operadores
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "**": 3
        }

    # --------------------------------------------------------
    # TOKENIZAÇÃO
    # --------------------------------------------------------
    def tokenize(self, expr):

        token_pattern = r"""
            ([+-]?\d+(\.\d+)?[+-]\d+(\.\d+)?i |[+-]?\d+(\.\d+)?i | [+-]?\d+(\.\d+)? | [+-]?i) | # números complexos ou reais
            (\*\*) |    # **
            [()+\-*/] | # operadores simples
            (conj|raiz) # funções
        """

        expr = expr.replace(" ", "")

        raw = re.findall(token_pattern, expr, flags=re.VERBOSE)

        # cada match tem 3 grupos — escolhemos o grupo não vazio
        tokens = [a or b or c for a, b, c in raw]

        return tokens

    # --------------------------------------------------------
    # PARSER / SHUNTING YARD → AST
    # --------------------------------------------------------
    def parse(self, expr):

        tokens = self.tokenize(expr)
        output = []
        ops = []

        def aplicar():
            op = ops.pop()

            # funções — unárias
            if op in ("conj", "raiz"):
                child = output.pop()
                output.append(UnaryOpNode(op, child))
                return

            # operadores binários
            right = output.pop()
            left = output.pop()
            output.append(BinaryOpNode(op, left, right))

        i = 0
        while i < len(tokens):

            t = tokens[i]

            # -----------------------------------
            # NÚMEROS (reais ou complexos)
            # -----------------------------------
            if re.match(r".*i$|^\d+(\.\d+)?$", t):
                real, imag = self.parse_complex_literal(t)
                numero = Complexo(real, imag)
                output.append(NumberNode(numero))

            # -----------------------------------
            # FUNÇÕES: conj, raiz
            # -----------------------------------
            elif t in ("conj", "raiz"):
                ops.append(t)

            # -----------------------------------
            # ABRE PARÊNTESE
            # -----------------------------------
            elif t == "(":
                ops.append("(")

            # -----------------------------------
            # FECHA PARÊNTESE
            # -----------------------------------
            elif t == ")":
                while ops and ops[-1] != "(":
                    aplicar()
                ops.pop()  # remove "("

                # função antes de "("
                if ops and ops[-1] in ("conj", "raiz"):
                    aplicar()

            # -----------------------------------
            # OPERADORES
            # -----------------------------------
            elif t in self.precedence:
                while (ops and ops[-1] in self.precedence
                       and self.precedence[ops[-1]] >= self.precedence[t]):
                    aplicar()
                ops.append(t)

            # -----------------------------------
            # POTÊNCIA **
            # -----------------------------------
            elif t == "**":
                while ops and ops[-1] == "**":
                    aplicar()
                ops.append(t)

            i += 1

        # aplica o restante
        while ops:
            aplicar()

        return output[-1]

    # --------------------------------------------------------
    # Extração de números complexos → (real, imag)
    # --------------------------------------------------------
    def parse_complex_literal(self, s: str):
        s = s.strip().replace(" ", "")

        # caso: real puro
        if "i" not in s:
            return float(s), 0.0

        # caso: só imaginário
        if s.endswith("i"):
            base = s[:-1]

            if base == "" or base == "+":
                return 0.0, 1.0
            if base == "-":
                return 0.0, -1.0

            # exemplo: 3i, 2.5i
            if "+" not in base and "-" not in base[1:]:
                return 0.0, float(base)

        # caso: a+bi ou a-bi
        m = re.match(r"^([+-]?\d+(\.\d+)?)([+-]\d+(\.\d+)?)i$", s)
        if m:
            real = float(m.group(1))
            imag = float(m.group(3))
            return real, imag

        raise ValueError(f"Literal complexo inválido: {s}")
