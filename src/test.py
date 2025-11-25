from parser import Parser
from executor import pre_process_expr, eval_node
from arvore import lisp, arvore


def testar(expr):
    print("======================================")
    print(f"Expressão: {expr}")
    try:
        arvore = parse(expr)
        lisp = to_lisp(arvore)
        print(f"LISP: {lisp}")
        print("Árvore visual:")
        print_tree(arvore)
        resultado = avaliar(arvore)
        print(f"Resultado: {resultado}")
    except Exception as e:
        print("ERRO:", e)
    print("======================================\n")


def main():
    testes = [
        "1+2",
        "3+4i",
        "1+2i + 3-4i",
        "-(2+3i)",
        "conj(3+4i)",
        "2*(3+4i)",
        "(1+2i)*(1-2i)",
        "1/(1+1i)",
        "2**3",
        "(1+1i)**2",
        "raiz(9,2)",
        "raiz(1+3i, 2)",
        "raiz(8, 1/3)",
        "raiz(10+4i, 2-3i)",
        "3 + -2",
        "3 - -2",
        "-i * (2+3i)"
    ]

    for t in testes:
        testar(t)


if __name__ == "__main__":
    main()