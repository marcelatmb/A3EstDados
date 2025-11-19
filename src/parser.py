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
        # precedência dos operadores (maior valor = maior precedência)
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "**": 4  # mais alto; trataremos associatividade à direita
        }

    # --------------------------------------------------------
    # TOKENIZAÇÃO
    # --------------------------------------------------------
    def tokenize(self, expr):

        expr = expr.replace(" ", "")

        token_pattern = r"""
            (\*\*) |
            ([+-]?\d+(\.\d+)?[+-]\d+(\.\d+)?i) |   # a+bi ou a-bi (com coeficientes)
            ([+-]?\d+(\.\d+)?i) |                 # bi (ex.: 3i, -2.5i)
            ([+-]?i) |                            # i, -i, +i
            ([+-]?\d+(\.\d+)?) |                  # número real com sinal opcional
            (conj|raiz) |                         # funções
            ([()+\-*/])                           # parênteses e operadores simples
        """

        raw_iter = re.finditer(token_pattern, expr, flags=re.VERBOSE)
        tokens = [m.group(0) for m in raw_iter]

        # valida: concatenando os tokens deve dar a string original
        if "".join(tokens) != expr:
            # achou algo que não foi tokenizado
            raise ValueError(f"Tokenização falhou em: {expr}. Tokens parciais: {tokens}")

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
            if re.match(r'^[+-]?\d+(\.\d+)?i$|^[+-]?i$|^[+-]?\d+(\.\d+)?$', t):
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
                if not ops:
                    raise ValueError("Parênteses desbalanceados")
                ops.pop()  # remove "("

                # função antes de "("
                if ops and ops[-1] in ("conj", "raiz"):
                    aplicar()

            # -----------------------------------
            # OPERADORES (inclui **)
            # -----------------------------------
            elif t in self.precedence:
                # respetar associatividade: ** é right-associative
                while (ops and ops[-1] in self.precedence and
                       ((self.precedence[ops[-1]] > self.precedence[t]) or
                        (self.precedence[ops[-1]] == self.precedence[t] and t != "**"))):
                    aplicar()
                ops.append(t)

            else:
                raise ValueError(f"Token inesperado: {t}")

            i += 1

        # aplica o restante
        while ops:
            if ops[-1] == "(":
                raise ValueError("Parênteses desbalanceados ao final")
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
        
        # casos especiais: i, +i, -i
        if s in ("i", "+i"):
            return 0.0, 1.0
        if s == "-i":
            return 0.0, -1.0

        # caso: a+bi ou a-bi (ex.: 3+4i, -2.5-0.1i)
        m = re.match(r"^([+-]?\d+(\.\d+)?)([+-]\d+(\.\d+)?)i$", s)
        if m:
            real = float(m.group(1))
            imag = float(m.group(3))
            return real, imag

        # caso: só imaginário como 3i ou -2.5i
        m2 = re.match(r"^([+-]?\d+(\.\d+)?)i$", s)
        if m2:
            return 0.0, float(m2.group(1))

        raise ValueError(f"Literal complexo inválido: {s}")
