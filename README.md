# A3EstDados

# Relatório do Projeto -- Parser e Calculadora de Expressões

## 1\. Identificação do Trabalho

**Disciplina: Estrutura de dados e análise de algoritmos**  
**Professor: Wellington Silveira**

-----

## 2\. Integrantes do Grupo

-   Marcela Tourinho Machado Barreto --- RA 12724139040
-   Erick Lopes Niesprodzinski --- RA 12724218402
-   Diego de Lima Gomes --- RA 12724124220
-   Luiggi Souza Grassi --- RA 12724143600

-----

## 3\. Repositório do Projeto

**GitHub:**  
[https://github.com/marcelatmb/A3EstDados](https://github.com/marcelatmb/A3EstDados)

-----

## 4\. Objetivo do Trabalho

Desenvolver uma calculadora com parser próprio para interpretar e
avaliar expressões matemáticas, incluindo números complexos, operadores
unários e binários, comparações e geração de árvores sintáticas.

-----

## 5\. Tecnologias Utilizadas

  * **Python**
  * **VSCode**
  * **GitHub**

-----

## 6\. Como Rodar o Código no VSCode

1.  Abra o VSCode.

2.  Vá em *File \> Open Folder* e selecione a pasta do projeto.

3.  Abra o arquivo principal (`executor.py`).

4.  Abra o terminal integrado: *Terminal \> New Terminal*.

5.  Execute o arquivo principal:

    ```bash
    python executor.py
    ```

6.  O programa iniciará com o prompt ` Expressão >  `.

**Pré-requisitos:**\\

  * Python instalado
  * VSCode instalado
  * Extensão Python habilitada

-----

## 7\. Como Usar a Calculadora

A calculadora aceita expressões matemáticas em uma única linha e suporta números complexos, variáveis, operadores binários, operadores unários e funções embutidas.

### **7.1 Operadores Aritméticos**

| Operação | Símbolo | Precedência | Exemplo |
| :--- | :--- | :--- | :--- |
| Soma | `+` | Baixa | `3 + 5i` |
| Subtração | `-` | Baixa | `10 - x` |
| Multiplicação | `*` | Média | `2 * 6` |
| Divisão | `/` | Média | `8 / 2i` |
| **Exponenciação** | `**` | Alta (direita) | `(1+i) ** 2` |
| **Multiplicação Implícita** | (Nenhum) | Média | `2(3+i)` ou `4x` |

### **7.2 Operadores Unários**

| Operador | Símbolo | Significado | Exemplo | Como a AST trata |
| :--- | :--- | :--- | :--- | :--- |
| Negação | `-` | Troca de sinal | `-5` | `u-` |
| Identidade | `+` | Sinal positivo | `+7` | `u+` |

**Exemplo:**  
Entrada: `-1i`  
AST: `(u- (0.0 + 1.0i))`

### **7.3 Números Complexos e Variáveis**

  * **Números Reais:** `5`, `-3.2`
  * **Números Imaginários:** `3i`, `-7.5i`. A letra usada para a unidade imaginária é sempre **i**.
  * **Unidade Imaginária Pura:** O símbolo `i` sozinho é reconhecido como $0 + 1i$.
  * **Números Complexos:** `2 + 5i`, `3 - 4i` (a ordem é importante na entrada de variáveis, conforme a Seção 7.7).
  * **Variáveis:** Qualquer sequência de letras, números e *underscore* começando com letra (ex.: `x`, `delta`, `z1`).

### **7.4 Funções e Raiz**

| Função | Sintaxe | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| **Conjugado** | `conj(z)` | Retorna o conjugado de $z$. | `conj(3 + 4i)` |
| **Raiz N-ésima** | `raiz(base, ordem)` | Calcula a raiz de ordem $n$ da base, i.e., $\text{base}^{1/\text{ordem}}$. **A ordem deve ser fornecida.** | `raiz(9, 2)` (raiz quadrada) |
| **Conjugado (implícito)** | `conj z` | Aceita a forma sem parênteses. | `conj (3+x)` |

### **7.5 Comparações Suportadas**

| Comparação | Símbolo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| Igualdade | `=` | Testa se o valor da esquerda é (aproximadamente) igual ao da direita. | `(3 + i) = (3 + 1i)` |

> *Nota: Apenas a comparação de igualdade (`=`) é suportada pelo parser implementado.*

### **7.6 Parênteses**

A calculadora respeita a **precedência de operadores** e o uso de parênteses:
Exemplo: `(3 + 2i) * 4` é diferente de `3 + 2i * 4`.

### **7.7 Entrada de Variáveis (Runtime)**

Se a expressão contiver variáveis (ex.: `x + y`), o programa solicitará o valor de cada variável, esperando um número complexo no formato `a+bi` ou real/imaginário simplificado (ex.: `5`, `-3i`, `1+1i`).

-----

## 8\. Arquitetura e Funcionamento

### **Tokenização**

Fragmenta a expressão de entrada (`text`) em uma lista de **Tokens**. Cada token representa um elemento básico da linguagem, como números reais (`NUMBER`), números imaginários (`IMAG`), operadores (`PLUS`, `TIMES`), ou nomes de variáveis/funções (`NAME`).

### **Parser**

O parser consome os tokens e, seguindo as regras de precedência da gramática, constrói a **Árvore Sintática Abstrata (AST)**. Essa estrutura hierárquica é composta pelos nós:

  * `NumberNode`: Para valores numéricos (complexos).
  * `VariableNode`: Para nomes de variáveis.
  * `UnaryOpNode`: Para operadores unários (ex.: `u-`, `conj`).
  * `BinaryOpNode`: Para operadores binários (ex.: `+`, `*`, `**`, `=`).

Exemplo:
Entrada: `-1i * 8 = 9`
AST (Notação LISP): `(= (* (u- (0.0 + 1.0i)) 8.0) 9.0)`

### **Executor**

O executor percorre a AST de forma recursiva (pós-ordem, para binários) e avalia o resultado de cada nó.

  * **Avaliação:** Em cada nó de operação, aplica a lógica matemática correspondente usando a classe `Complexo`.
  * **Variáveis:** Coleta as variáveis presentes na AST e solicita seus valores ao usuário antes de iniciar o cálculo.
  * **Tratamento de Erros:** Lança `ErroMatematico` em casos como divisão por zero.

-----

## 9\. Exemplo de Funcionamento Completo

**Entrada:**

```
(1 + i)**2 = 2i
```

**Árvore (LISP):**

```
(= (** (1.0 + 1.0i) (2.0 + 0.0i)) (0.0 + 2.0i))
```

**Árvore (visual):**

```
└── BinaryOp: =
        └── BinaryOp: **
                └── Number: 1.0 + 1.0i
                └── Number: 2.0 + 0.0i
        └── Number: 0.0 + 2.0i
```

**Resultado:**

```
True
```

-----

## 10\. Conclusão

O projeto permitiu explorar na prática:

  * A construção de um **parser completo** (análise léxica e sintática).
  * Manipulação de expressões com **números complexos e imaginários**.
  * Implementação de operadores unários, binários e funções embutidas.
  * Uso e avaliação de **Árvores Sintáticas Abstratas (AST)**.
  * A organização modular em classes (`Complexo`, `Token`, `Parser`, `...Node`).

A calculadora demonstra ser capaz de interpretar e avaliar expressões matemáticas complexas de forma consistente, modular e robusta contra erros de sintaxe ou matemáticos.