# parser.py
# ============================================================
# Parser de expressões para a calculadora de números complexos
# Produz uma AST com nós: NumberNode, VariableNode, UnaryOpNode, BinaryOpNode
# Suporta: números reais, imaginários (ex.: 3i), + - * / ** =, conj(...), raiz(...),
#          parênteses e multiplicação implícita (ex.: 2(3+1) ou 3i(1+2))
# ============================================================

import re
from complexos import Complexo

# ------------------ tokens ------------------
TOKEN_SPEC = [
    ("POW",    r"\*\*"),
    ("IMAG",   r"\d+(\.\d+)?i"),     # 5i antes de 5
    ("NUMBER", r"\d+(\.\d+)?"),
    ("PLUS",   r"\+"),
    ("MINUS",  r"-"),
    ("TIMES",  r"\*"),
    ("DIV",    r"/"),
    ("EQ",     r"="),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COMMA",  r","),
    ("NAME",   r"[A-Za-z_]\w*"),
    ("SKIP",   r"[ \t]+"),
    ("MISMATCH", r"."),
]

TOKEN_REGEX = "|".join(f"(?P<{name}>{regex})" for name, regex in TOKEN_SPEC)

# ------------------ token class ------------------
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# ------------------ AST nodes (compatíveis com executor/arvore) ------------------
class NumberNode:
    def __init__(self, value: Complexo):
        self.value = value
    def __repr__(self):
        return f"NumberNode({self.value})"

class VariableNode:
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return f"VariableNode({self.name})"

class UnaryOpNode:
    def __init__(self, op: str, child):
        self.op = op
        self.child = child
    def __repr__(self):
        return f"UnaryOpNode({self.op}, {self.child})"

class BinaryOpNode:
    def __init__(self, op: str, left, right):
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self):
        return f"BinaryOpNode({self.op}, {self.left}, {self.right})"

# ------------------ Parser ------------------
class Parser:
    def __init__(self):
        pass

    # interface pública: parse(text) -> AST root
    def parse(self, text: str):
        self.tokens = self.tokenize(text)
        self.pos = 0
        if not self.tokens:
            raise SyntaxError("Expressão vazia")
        node = self.expression()
        if self.current_type() != "EOF":
            raise SyntaxError(f"Token extra após expressão: {self.current()}")
        return node

    # tokenização
    def tokenize(self, text: str):
        tokens = []
        for m in re.finditer(TOKEN_REGEX, text):
            type_ = m.lastgroup
            value = m.group()
            if type_ == "SKIP":
                continue
            if type_ == "MISMATCH":
                raise SyntaxError(f"Caractere inválido: {value}")
            if type_ == "NUMBER":
                tokens.append(Token("NUMBER", float(value)))
            elif type_ == "IMAG":
                tokens.append(Token("IMAG", float(value[:-1])))
            elif type_ == "NAME":
                tokens.append(Token("NAME", value))
            else:
                tokens.append(Token(type_, value))
        tokens.append(Token("EOF", None))
        return tokens

    # ----------------- gramática com precedências -----------------
    # expression -> sum_expr ( EQ sum_expr )?
    def expression(self):
        left = self.sum_expr()
        if self.current_type() == "EQ":
            op_tok = self.eat("EQ")
            right = self.sum_expr()
            return BinaryOpNode(op_tok.value, left, right)
        return left

    # sum_expr -> term ((PLUS|MINUS) term)*
    def sum_expr(self):
        node = self.term()
        while self.current_type() in ("PLUS", "MINUS"):
            op_tok = self.eat(self.current_type())
            right = self.term()
            node = BinaryOpNode(op_tok.value, node, right)
        return node

    # term -> power ((TIMES|DIV) power | implicit_mul power)*
    def term(self):
        node = self.power()
        starts_factor = ("NUMBER", "IMAG", "LPAREN", "NAME")
        while True:
            if self.current_type() in ("TIMES", "DIV"):
                op_tok = self.eat(self.current_type())
                right = self.power()
                node = BinaryOpNode(op_tok.value, node, right)
                continue
            # multiplicação implícita (ex.: 2(3+1), 3i(1+2), x y)
            if self.current_type() in starts_factor:
                right = self.power()
                node = BinaryOpNode("*", node, right)
                continue
            break
        return node

    # power -> factor (POW power)?  (right-assoc)
    def power(self):
        node = self.factor()
        if self.current_type() == "POW":
            op_tok = self.eat("POW")
            right = self.power()
            node = BinaryOpNode(op_tok.value, node, right)
        return node

    # factor -> (PLUS|MINUS) factor | NUMBER | IMAG | LPAREN expression RPAREN |
    #           NAME (funções conj(...) e raiz(...)) | NAME (variável)
    def factor(self):
        tok = self.current()
        if tok.type == "PLUS":
            self.eat("PLUS")
            child = self.factor()
            return UnaryOpNode("u+", child)
        if tok.type == "MINUS":
            self.eat("MINUS")
            child = self.factor()
            return UnaryOpNode("u-", child)
        if tok.type == "NUMBER":
            t = self.eat("NUMBER")
            return NumberNode(Complexo(t.value, 0.0))
        if tok.type == "IMAG":
            t = self.eat("IMAG")
            return NumberNode(Complexo(0.0, t.value))
        if tok.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expression()
            self.eat("RPAREN")
            return node
        if tok.type == "NAME":
            name_tok = self.eat("NAME")
            name = name_tok.value.lower()
            # funções com parênteses
            if self.current_type() == "LPAREN":
                self.eat("LPAREN")
                if name == "conj":
                    child = self.expression()
                    self.eat("RPAREN")
                    return UnaryOpNode("conj", child)
                elif name == "raiz":
                    left = self.expression()
                    self.eat("COMMA")
                    right = self.expression()
                    self.eat("RPAREN")
                    return BinaryOpNode("raiz", left, right)
                else:
                    raise SyntaxError(f"Função desconhecida: {name}")
            # conj sem parênteses: conj x
            if name == "conj":
                child = self.factor()
                return UnaryOpNode("conj", child)
            # senão é variável
            return VariableNode(name_tok.value)
        raise SyntaxError(f"Token inesperado em factor(): {tok}")

    # ----------------- auxiliares -----------------
    def current(self):
        if self.pos >= len(self.tokens):
            return Token("EOF", None)
        return self.tokens[self.pos]

    def current_type(self):
        return self.current().type

    def eat(self, type_):
        tok = self.current()
        if tok.type == type_:
            self.pos += 1
            return tok
        raise SyntaxError(f"Esperado {type_}, encontrado {tok.type} ({tok.value})")
