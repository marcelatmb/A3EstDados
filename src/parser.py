import re
from complexos import Complexo

class Node: pass

class NumberNode(Node):
    def __init__(self, value):
        self.value = value   # instância de Complexo
    def __repr__(self):
        return f"Number({repr(self.value)})"

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

class Parser:
    def __init__(self):
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "**": 4
        }

    def tokenize(self, expr):
        expr = expr.replace(" ", "")

        token_pattern = r'''
            (\()                 |   # abre parênteses
            (\))                 |   # fecha parênteses
            (\*\*)               |   # potência
            (\+)                 |   # +
            (\-)                 |   # -
            (\*)                 |   # *
            (\/)                 |   # /
            ([+-]?\d+(?:\.\d+)?[+-]\d+(?:\.\d+)?i)  |  # a+bi ou a-bi (com coeficientes)
            ([+-]?\d+(?:\.\d+)?i)  |   # bi (ex.: 3i, -2.5i)
            ([+-]?i)              |   # i, -i, +i
            ([+-]?\d+(?:\.\d+)?)      # número real com sinal opcional
        '''

        raw_iter = re.finditer(token_pattern, expr, flags=re.VERBOSE)
        tokens = [m.group(0) for m in raw_iter]

        if "".join(tokens) != expr:
            raise ValueError(f"Tokenização falhou em: {expr}. Tokens parciais: {tokens}")

        return tokens

    def parse(self, expr):
        tokens = self.tokenize(expr)
        output = []
        ops = []

        def aplicar():
            op = ops.pop()
            if op in ("conj", "raiz"):
                child = output.pop()
                output.append(UnaryOpNode(op, child))
                return
            right = output.pop()
            left = output.pop()
            output.append(BinaryOpNode(op, left, right))

        i = 0
        while i < len(tokens):
            t = tokens[i]

            if re.match(r'^[+-]?\d+(\.\d+)?i$|^[+-]?i$|^[+-]?\d+(\.\d+)?$', t):
                real, imag = self.parse_complex_literal(t)
                numero = Complexo(real, imag)
                output.append(NumberNode(numero))
            elif t in ("conj", "raiz"):
                ops.append(t)
            elif t == "(":
                ops.append("(")
            elif t == ")":
                while ops and ops[-1] != "(":
                    aplicar()
                if not ops:
                    raise ValueError("Parênteses desbalanceados")
                ops.pop()
                if ops and ops[-1] in ("conj", "raiz"):
                    aplicar()
            elif t in self.precedence:
                while (ops and ops[-1] in self.precedence and
                       ((self.precedence[ops[-1]] > self.precedence[t]) or
                        (self.precedence[ops[-1]] == self.precedence[t] and t != "**"))):
                    aplicar()
                ops.append(t)
            else:
                raise ValueError(f"Token inesperado: {t}")

            i += 1

        while ops:
            if ops[-1] == "(":
                raise ValueError("Parênteses desbalanceados ao final")
            aplicar()

        return output[-1]

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
            real = float(m.group(1))
            imag = float(m.group(3))
            return real, imag
        m2 = re.match(r"^([+-]?\d+(\.\d+)?)i$", s)
        if m2:
            return 0.0, float(m2.group(1))
        raise ValueError(f"Literal complexo inválido: {s}")
