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
            n_int = int(n.a)
            r = self.modulo()
            teta = self.argumento()
            rn = pow(r, n_int)
            ang = n_int * teta
            return Complexo(
                round(rn * math.cos(ang), 10),
                round(rn * math.sin(ang), 10)
            )

        # caso geral: z^n = exp(n * ln(z))
        r = self.modulo()
        
