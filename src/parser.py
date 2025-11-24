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
        # Apenas 'conj' é um operador unário de palavra-chave explícito
        self.precedence.update({"conj": 5})

    def tokenize(self, expr):
        expr = expr.replace(" ", "")

        # Padrão compacto e robusto. 'raiz' foi removido.
        token_pattern = r'(\*\*)|(conj)|([+-]?\d+(?:\.\d+)?[+-]\d+(?:\.\d+)?i)|([+-]?\d+(?:\.\d+)?i)|([+-]?i)|([+-]?\d+(?:\.\d+)?)|(\()|(\))|(\+)|(\-)|(\*)|(\/)'

        raw_iter = re.finditer(token_pattern, expr)
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
            # 'raiz' removido daqui
            if op in ("conj"):
                child = output.pop()
                output.append(UnaryOpNode(op, child))
                return
            right = output.pop()
            left = output.pop()
            output.append(BinaryOpNode(op, left, right))

        i = 0
        while i < len(tokens):
            t = tokens[i]

            # 1. TRATAMENTO DE LITERAIS (Números complexos/reais)
            if re.match(r'^[+-]?\d+(\.\d+)?i$|^[+-]?i$|^[+-]?\d+(\.\d+)?[+-]\d+(\.\d+)?i$|^[+-]?\d+(\.\d+)?$', t):
                real, imag = self.parse_complex_literal(t)
                numero = Complexo(real, imag)
                output.append(NumberNode(numero))
            
            # 2. TRATAMENTO DE PALAVRAS-CHAVE E PARÊNTESES
            # 'raiz' removido daqui
            elif t in ("conj"):
                ops.append(t)
            elif t == "(":
                ops.append("(")
            elif t == ")":
                while ops and ops[-1] != "(":
                    aplicar()
                if not ops:
                    raise ValueError("Parênteses desbalanceados")
                ops.pop()
                # 'raiz' removido daqui
                if ops and ops[-1] in ("conj"): 
                    aplicar()
            
            # 3. TRATAMENTO DE OPERADORES BINÁRIOS E UNÁRIOS DE SINAL
            elif t in self.precedence:
                
                # Checa se o operador binário é na verdade um operador UNÁRIO DE SINAL
                is_unary_sign = (t in ('+', '-')) and \
                                (i == 0 or tokens[i-1] in ('(', '+', '-', '*', '/', '**'))
                                
                if is_unary_sign:
                    # Se for um sinal unário, ele é empilhado. Será aplicado como UnaryOpNode
                    # na função aplicar() ou tratado como parte do próximo literal se for o caso.
                    ops.append(t)
                else:
                    # É um operador binário normal
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