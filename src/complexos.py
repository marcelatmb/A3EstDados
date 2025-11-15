import math

class Complexo:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        a = self.a + other.a
        b = self.b + other.b
        return Complexo(a, b)
    
    def __sub__(self, other):
        a = self.a - other.a
        b = self.b - other.b
        return Complexo(a, b)

    def __mul__(self, other):
        real1 = self.a
        imag1 = self.b
        real2 = other.a
        imag2 = other.b
        a = (real1 * real2) + (imag1 * imag2 * (-1))
        b = (real1 * imag2) + (imag1 * real2)
        return Complexo(a, b)
    
    def __truediv__(self, other):
        if (other.a == 0) and (other.b == 0):
            raise Exception("Impossível dividir um número por 0")
        
        numerador = self * other.conjug()
        denominador = other.a**2 + other.b**2
        return Complexo(numerador.a / denominador, numerador.b / denominador)
    
    def __pow__(self, n):
        r = self.modulo()
        teta = self.argumento()
        rn = pow(r, n)
        ang = n * teta
        a = rn * math.cos(ang)
        b = rn * math.sin(ang)
        return Complexo(round(a, 10), round(b, 10))
    
    def raiz(self, n):
        if n == 0 :
            raise Exception("Impossível raiz indicie 0")

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

    def conjug(self):
        a = self.a
        b = -self.b
        return Complexo(a, b)
    
    def modulo(self):
        return math.sqrt(self.a**2 + self.b**2)
    
    def argumento(self):
        return math.atan2(self.b, self.a)
    
    def __eq__(self, other):
        return (self.a == other.a) and (self.b == other.b)
    
    def __str__(self):
        if self.b == 0:
            return f'{self.a}'
        elif self.b > 0:
            return f'{self.a} + {self.b}i'
        else:
            return f'{self.a} - {self.b * (-1)}i'
