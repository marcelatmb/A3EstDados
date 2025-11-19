import math
import re


# ============================================================
#                CLASSE PARA NÚMEROS COMPLEXOS
# ============================================================
# Representa um número do tipo:
#     z = a + bi
# onde:
#     a → parte real
#     b → parte imaginária
#
# A classe implementa:
# - operações aritméticas (+, -, *, /)
# - potência z**n (com casos inteiro e geral)
# - exponencial complexa
# - raízes n-ésimas
# - módulo, argumento, conjugado
#
# Além disso, sempre que necessário converte automaticamente
# valores numéricos comuns (int, float) para Complexo.
# ============================================================

class Complexo:

    def __init__(self, a, b=0):
        """
        Construtor do número complexo.

        - Se 'a' já for Complexo: copia seus valores.
        - Caso contrário: interpreta 'a' como parte real
          e 'b' como parte imaginária.
        """
        if isinstance(a, Complexo):
            self.a = a.a
            self.b = a.b
        else:
            self.a = a
            self.b = b

    # --------------------------------------------------------
    # SOMA: z1 + z2
    # --------------------------------------------------------
    def __add__(self, other):
        other = self._cast(other)
        return Complexo(self.a + other.a, self.b + other.b)
    
    def __radd__(self, other):
        # permite: número + Complexo
        return self.__add__(other)

    # --------------------------------------------------------
    # SUBTRAÇÃO: z1 - z2
    # --------------------------------------------------------
    def __sub__(self, other):
        other = self._cast(other)
        return Complexo(self.a - other.a, self.b - other.b)
    
    def __rsub__(self, other):
        # permite: número - Complexo
        other = self._cast(other)
        return other.__sub__(self)

    # --------------------------------------------------------
    # MULTIPLICAÇÃO: (a+bi)(c+di)
    # --------------------------------------------------------
    def __mul__(self, other):
        other = self._cast(other)
        return Complexo(
            self.a * other.a - self.b * other.b,
            self.a * other.b + self.b * other.a
        )
    
    def __rmul__(self, other):
        return self.__mul__(other)

    # --------------------------------------------------------
    # DIVISÃO: z1 / z2 usando conjugado
    # --------------------------------------------------------
    def __truediv__(self, other):
        other = self._cast(other)

        if other.a == 0 and other.b == 0:
            raise ZeroDivisionError("divisão por zero")

        num = self * other.conjug()
        den = other.a**2 + other.b**2

        return Complexo(num.a / den, num.b / den)
    
    def __rtruediv__(self, other):
        other = self._cast(other)
        return other.__truediv__(self)

    # --------------------------------------------------------
    # POTÊNCIA z ** n
    # - caso n inteiro: usa forma trigonométrica
    # - caso geral: usa log(z) e exp
    # --------------------------------------------------------
    def __pow__(self, n):
        n = self._cast(n)

        # caso especial: expoente inteiro (parte imaginária 0)
        if n.b == 0 and float(n.a).is_integer():
            n = int(n.a)
            r = self.modulo()
            teta = self.argumento()
            rn = pow(r, n)
            ang = n * teta
            return Complexo(
                round(rn * math.cos(ang), 10),
                round(rn * math.sin(ang), 10)
            )

        # caso geral: z^n = exp(n * ln(z))
        r = self.modulo()
        t = self.argumento()
        lnz = Complexo(math.log(r), t)
        return (n * lnz).exp()

    # --------------------------------------------------------
    # EXPONENCIAL COMPLEXA: e^(a+bi)
    # --------------------------------------------------------
    def exp(self):
        ea = math.exp(self.a)
        return Complexo(
            ea * math.cos(self.b),
            ea * math.sin(self.b)
        )

    # --------------------------------------------------------
    # RAÍZES n-ÉSIMAS DE z
    # Retorna uma lista com n raízes.
    # --------------------------------------------------------
    def raiz(self, n=2):
        if n == 0:
            raise ZeroDivisionError("índice da raiz não pode ser zero")

        resultados = []
        r = self.modulo()
        teta = self.argumento()
        rn = pow(r, 1/n)

        for k in range(n):
            ang = (teta + 2 * math.pi * k) / n
            resultados.append(Complexo(
                round(rn * math.cos(ang), 10),
                round(rn * math.sin(ang), 10)
            ))

        return resultados

    # --------------------------------------------------------
    # MÓDULO: |z|
    # --------------------------------------------------------
    def modulo(self):
        return math.sqrt(self.a**2 + self.b**2)
    
    # --------------------------------------------------------
    # ARGUMENTO: arg(z)
    # --------------------------------------------------------
    def argumento(self):
        return math.atan2(self.b, self.a)

    # --------------------------------------------------------
    # CONJUGADO: a - bi
    # --------------------------------------------------------
    def conjug(self):
        return Complexo(self.a, -self.b)
    
    # --------------------------------------------------------
    # Converte valores numéricos comuns para Complexo
    # --------------------------------------------------------
    def _cast(self, x):
        if isinstance(x, Complexo):
            return x
        return Complexo(float(x), 0)

    # --------------------------------------------------------
    # IGUALDADE aproximada (tolerância numérica)
    # --------------------------------------------------------
    def __eq__(self, other):
        other = self._cast(other)
        return abs(self.a - other.a) < 1e-9 and abs(self.b - other.b) < 1e-9
    
    # --------------------------------------------------------
    # Representação amigável: "a + bi"
    # --------------------------------------------------------
    def __str__(self):
        if self.b == 0:
            return f"{self.a}"
        if self.b > 0:
            return f"{self.a} + {self.b}i"
        return f"{self.a} - {abs(self.b)}i"
