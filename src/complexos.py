import math

class ErroMatematico(Exception):
    pass

class Complexo:
    def __init__(self, a, b=0.0):
        if isinstance(a, Complexo):
            self.a = float(a.a)
            self.b = float(a.b)
        else:
            self.a = float(a)
            self.b = float(b)

    # representação
    def __repr__(self):
        return f"Complexo({self.a}, {self.b})"

    def __str__(self):
        a = self.a
        b = self.b
        if b == 0:
            return f"{a}"
        if a == 0:
            return f"{b}i"
        if b > 0:
            return f"{a} + {b}i"
        return f"{a} - {-b}i"

    # cast helper
    @staticmethod
    def _cast(val):
        if isinstance(val, Complexo):
            return val
        if isinstance(val, (int, float)):
            return Complexo(float(val), 0.0)
        raise TypeError("Operação com tipo incompatível")

    # soma/subtração
    def __add__(self, other):
        other = Complexo._cast(other)
        return Complexo(self.a + other.a, self.b + other.b)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = Complexo._cast(other)
        return Complexo(self.a - other.a, self.b - other.b)

    def __rsub__(self, other):
        other = Complexo._cast(other)
        return Complexo(other.a - self.a, other.b - self.b)

    # multiplicação
    def __mul__(self, other):
        other = Complexo._cast(other)
        return Complexo(
            self.a * other.a - self.b * other.b,
            self.a * other.b + self.b * other.a
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    # divisão
    def __truediv__(self, other):
        other = Complexo._cast(other)
        if other.a == 0 and other.b == 0:
            raise ErroMatematico("divisão por zero")
        den = other.a * other.a + other.b * other.b
        # multiplicar pelo conjugado do denominador
        num = self * other.conjugado()
        return Complexo(num.a / den, num.b / den)

    def __rtruediv__(self, other):
        other = Complexo._cast(other)
        return other.__truediv__(self)

    # conjugado
    def conjugado(self):
        return Complexo(self.a, -self.b)

    # módulo e argumento
    def modulo(self):
        return math.hypot(self.a, self.b)

    def argumento(self):
        return math.atan2(self.b, self.a)

    # potência (apoiando expoente real/inteiro e complexo)
    def __pow__(self, n):
        # aceitar int/float/Complexo
        if isinstance(n, (int, float)):
            n = Complexo(float(n), 0.0)
        elif not isinstance(n, Complexo):
            raise TypeError("Expoente inválido")

        # caso expoente inteiro real -> fórmula de De Moivre
        if n.b == 0 and float(n.a).is_integer():
            k = int(n.a)
            r = self.modulo()
            theta = self.argumento()
            rn = (r ** k)
            ang = k * theta
            return Complexo(rn * math.cos(ang), rn * math.sin(ang))

        # caso geral: z^w = exp(w * ln(z))
        # ln(z) = ln(r) + i*theta
        r = self.modulo()
        if r == 0:
            if n.a == 0 and n.b == 0:
                return Complexo(1, 0)
            return Complexo(0, 0)
        ln_r = math.log(r)
        theta = self.argumento()
        # w * ln(z)
        x = n.a * ln_r - n.b * theta
        y = n.a * theta + n.b * ln_r
        # exp(x + i y) = exp(x) * (cos(y) + i sin(y))
        expx = math.exp(x)
        return Complexo(expx * math.cos(y), expx * math.sin(y))

    # raiz (n-ésima raiz principal) - raiz sem argumento assume n=2
    '''def raiz_n(self, n=2):
        if n == 0:
            raise ErroMatematico("raiz de ordem zero")
        r = self.modulo()
        theta = self.argumento()
        raiz_r = r ** (1.0 / n)
        raiz_theta = theta / n
        return Complexo(raiz_r * math.cos(raiz_theta), raiz_r * math.sin(raiz_theta))'''

    # igualdade
    def __eq__(self, other):
        if not isinstance(other, Complexo):
            other = Complexo._cast(other)
        return abs(self.a - other.a) < 1e-9 and abs(self.b - other.b) < 1e-9
