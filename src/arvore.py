class no:
    def __init__(self,pai,esquerda=None,direita=None):
        self.pai=pai
        self.esquerda=esquerda
        self.direita=direita
        
 # def no, determina a direçao em arvore.
    def __repr__(self):
        return f"No({self.pai!r}, {self.esquerda!r}, {self.direita!r})"


# Funções criadoras de Nós
def no_operador (pai,esquerda,direita=None):
     return no (pai,esquerda,direita) 
# def operador, define os nos de operador
def no_numero (pai):
    return no(pai)

def no_variavel (pai):
    return no(pai)


# Funções que imprimem árvore
def lisp (no):
    if no is None:
        return""
    if no.esquerda is None and no.direita is None:
        return f"{no.pai}"
    if no.direita is None:
        return f"({no.pai} {lisp(no.esquerda)})"
    return f"({no.pai} {lisp(no.esquerda)} {lisp(no.direita)})"

def arvore(no,grau=0):
    if no is None:
        return
    arvore(no.direita, grau + 1)
    print("    " * grau + f"--->{no.pai}")

    arvore(no.esquerda, grau + 1)


# 3j + 5
# Criando um nó para 3j + 5
no_exemplo = no_operador("+", no_numero(3j), no_numero(5))
# Chamando a função que cria o LISP
print(lisp(no_exemplo))
# Chamando a função que cria a árvore
arvore(no_exemplo)

# raiz de -70
# Criando um nó para raiz de -70
no_exemplo2 = no_operador("raiz", no_numero(-70))
# Chamando a função que cria o LISP
print(lisp(no_exemplo2))
# Chamando a função que cria a árvore
arvore(no_exemplo2)

# (3j + 5) * (raiz de -70)
# Sabemos que (3j + 5) = no_exemplo e que (raiz de -70) = no_exemplo2
no_resultado = no_operador("*", no_exemplo, no_exemplo2)
# Chamando a função que cria o LISP
print(lisp(no_resultado))
# Chamando a função que cria a árvore
arvore(no_resultado)
