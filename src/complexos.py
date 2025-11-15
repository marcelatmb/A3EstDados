import math

class Complexo:

    def __init__(self, a, b=0):
        if isinstance(a, Complexo):
            self.a = a.a
            self.b = a.b
        else:
            self.a = a
            self.b = b

    def __add__(self, other):
        other = self._cast(other)
        a = self.a + other.a
        b = self.b + other.b
        return Complexo(a, b)
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self._cast(other)
        a = self.a - other.a
        b = self.b - other.b
        return Complexo(a, b)
    
    def __rsub__(self, other):
        other = self._cast(other)
        return other.__sub__(self)

    def __mul__(self, other):
        other = self._cast(other)
        a = (self.a * other.a) - (self.b * other.b)
        b = (self.a * other.b) + (self.b * other.a)
        return Complexo(a, b)
    
    def __rmul__(self, other):
        return self.__mul__(other)

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

    def __pow__(self, n):
        n = self._cast(n)

        if n.b == 0 and float(n.a).is_integer():
            n = int(n.a)
            r = self.modulo()
            teta = self.argumento()
            rn = pow(r, n)
            ang = n * teta
            a = rn * math.cos(ang)
            b = rn * math.sin(ang)
            return Complexo(round(a, 10), round(b, 10))

        r = self.modulo()
        t = self.argumento()

        lnz = Complexo(math.log(r), t)
        return (n * lnz).exp()

    def exp(self):
        ea = math.exp(self.a)
        a = ea * math.cos(self.b)
        b = ea * math.sin(self.b)
        return Complexo(a, b)

    def raiz(self, n):
        if n == 0:
            raise ZeroDivisionError("índice da raiz não pode ser zero")

        resultados = []
        r = self.modulo()
        teta = self.argumento()
        rn = pow(r, 1/n)

        for k in range(n):
            ang = (teta + 2 * math.pi * k) / n
            a = rn * math.cos(ang)
            b = rn * math.sin(ang)
            resultados.append(Complexo(round(a, 10), round(b, 10)))

        return resultados

    def modulo(self):
        return math.sqrt(self.a**2 + self.b**2)
    
    def argumento(self):
        return math.atan2(self.b, self.a)

    def conjug(self):
        return Complexo(self.a, -self.b)
    
    def _cast(self, x):
        if isinstance(x, Complexo):
            return x
        return Complexo(float(x), 0)

    def __eq__(self, other):
        other = self._cast(other)
        return abs(self.a - other.a) < 1e-9 and abs(self.b - other.b) < 1e-9
    
    def __str__(self):
        if self.b == 0:
            return f'{self.a}'
        if self.b > 0:
            return f'{self.a} + {self.b}i'
        return f'{self.a} - {abs(self.b)}i'
