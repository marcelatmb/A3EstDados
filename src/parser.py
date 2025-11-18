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
            (\d+\+\d+i|\d+-\d+i|\d+i|\d+|i) |   # números complexos ou reais
            (\*\*) |                            # **
            [()+\-*/] |                         # operadores simples
            (conj|raiz)                         # funções
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
            if re.match(r".*i$|^\d+$", t):
                numero = Complexo.from_string(t)
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

                # função imediatamente antes de "("
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
