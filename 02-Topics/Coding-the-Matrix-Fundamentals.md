---
tags: [phase-0, math, linear-algebra, coding-the-matrix]
status: learning
first_learned: 2026-07-01
last_reviewed: 2026-07-01
confidence: 2/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Coding the Matrix — Fundamentos (Klein)

Source: *Coding the Matrix: Linear Algebra through Computer Science Applications* (1st ed.), Philip N. Klein — PDF en `00-Meta/resources/Philip N. Klein-Coding the Matrix...pdf`

## 1. Cartesian product y cardinalidad (Cap 0.2, p.2)

**Idea simple:** el producto cartesiano $A \times B$ es el conjunto de TODOS los pares posibles combinando un elemento de A con uno de B. Pensalo como nested loop: por cada elemento de A, generás un par nuevo con cada elemento de B.

```
for a in A:
    for b in B:
        yield (a, b)
```

Total de pares generados = (cantidad de iteraciones del loop externo) × (cantidad de iteraciones del loop interno) = $|A| \times |B|$.

**Fórmula (Proposition 0.2.3, p.2):**
$$|A \times B| = |A| \cdot |B|$$

**Ejemplo verificado (Example 0.2.1 / Quiz 0.2.2, p.2):** $A=\{1,2,3\}$ ($|A|=3$), $B=\{\heartsuit,\spadesuit,\clubsuit,\diamondsuit\}$ ($|B|=4$) → $|A \times B| = 3 \times 4 = 12$ pares, coincide con la lista completa del ejemplo.

---

## 2. La función (Cap 0.3, p.2-3)

**Idea simple:** una función matemática es literalmente un **dict/hashmap** — cada input (key) mapea a exactamente un output (value), nunca a dos valores distintos. "Dominio" = el conjunto de keys válidas. "Imagen" (de un input específico) = el value que le corresponde. "Pre-imagen" = la key que produjo ese value.

**Definición formal (p.2-3):** una función es un conjunto de pares $(a,b)$ donde ningún par comparte la misma primera entrada (ningún key duplicado — si tuvieras dos pares con el mismo `a` pero distinto `b`, no sería función, sería ambigua).

$$f = \{(a,b) : \text{ningún par comparte la misma primera entrada } a\}$$

- **Dominio ($D$):** conjunto de todos los inputs posibles (todos los `a`).
- **Imagen de un input:** el output que le corresponde (`b`).
- **Pre-imagen de un output:** el input que lo produjo (`a`).

### Ejemplos citados

**Example 0.3.1 (p.2) — función de duplicar:** dominio $\{1,2,3,...\}$, función = $\{(1,2),(2,4),(3,6),(4,8),...\}$. Como código: `{n: 2*n for n in range(1, N)}`.

**Example 0.3.2 (p.2) — multiplicación:** el dominio puede ser en sí un producto cartesiano — acá dominio = $\{1,2,3,...\} \times \{1,2,3,...\}$ (pares de números), función = $\{((1,1),1),((1,2),2),((2,2),4),((2,3),6),...\}$. Osea: el input mismo es una tupla `(a,b)`, el output es `a*b`.

**Example 0.3.3 (p.3) — cifrado César:** cada letra se reemplaza por la que está 3 posiciones adelante en el alfabeto (con wraparound pa X,Y,Z). Dominio y codominio son el mismo conjunto: el alfabeto $\{A,B,...,Z\}$.

$$A \mapsto D,\ B \mapsto E,\ C \mapsto F,\ \ldots,\ X \mapsto A,\ Y \mapsto B,\ Z \mapsto C$$

`MATRIX` se encripta como `PDWULA` (cada letra +3, con wraparound). En código: literal un dict de 26 entradas, o `chr((ord(c)-65+3)%26+65)`.

**Por qué importa:** este ejemplo (dominio=codominio, cada input mapea a exactamente un output, y la función es invertible — se puede desencriptar restando 3) es la semilla de "función invertible" que después se conecta con **matriz invertible** en Cap 4 — misma idea, escalada a vectores.

---

## 3. Notación $F^D$ y función identidad (Cap 0.3.3-0.3.4, p.6)

**Idea simple:** $F^D$ no es una función — es el conjunto de TODAS las funciones posibles con dominio D y codominio F. Como pensar en todos los programas posibles con una firma de tipo dada, no un programa en particular.

**Por qué el exponente (Fact 0.3.9, p.6):** cada elemento del dominio elige independientemente uno de los valores del codominio. Multiplicás las opciones una vez por cada input:

$$|D^F| = |D|^{|F|}$$

Ejemplo: dominio 3 elementos, codominio 2 elementos → $2^3=8$ funciones distintas posibles (como contar combinaciones de bits, o dicts posibles con 3 keys fijas y values booleanos).

**Función identidad (p.6):** devuelve exactamente el input, sin modificarlo — el "no-op" de las funciones.

$$\text{id}_D(d) = d \quad \text{para todo } d \in D$$

En código: `lambda x: x`. Es el elemento neutro al componer funciones (igual rol que la matriz identidad $I$ en Cap 4 — multiplicar por $I$ no cambia nada).

---

## 4. Inverso funcional (Cap 0.3.7, p.7-8)

**Idea simple:** el inverso de una función "deshace" su efecto. Si `f` te lleva de A a B, su inverso `g` te trae de vuelta de B a A. Aplicar una y después la otra (en cualquier orden) = no-op, quedás donde empezaste.

**Ejemplo del cifrado César:** `f` = encriptar (+3 con wraparound). Su inverso `g` = desencriptar (-3 con wraparound). `encrypt(decrypt(x)) == x` y `decrypt(encrypt(x)) == x` pa todo x.

**Definición formal (0.3.13, p.7):** $f$ y $g$ son inversos funcionales si se cumplen LAS DOS condiciones (no alcanza con una sola dirección):

$$f \circ g = \text{id}_{\text{dominio de } g}$$
$$g \circ f = \text{id}_{\text{dominio de } f}$$

**No toda función es invertible.** Falla cuando dos inputs distintos mapean al mismo output (ej. $f(1)=5$ y $f(2)=5$) — el inverso no sabría si devolver 1 o 2 al ver un 5, hay ambigüedad. Función con inverso = *invertible*.

**Por qué importa:** esta idea exacta (invertibilidad, deshacer sin ambigüedad) se escala a matrices en Cap 4 — matriz invertible = misma lógica pero para transformaciones lineales completas, no solo funciones sobre un elemento.

---

## 5. Cap 4.1 — What is a matrix? (p.185-189)

### 4.1.1 Traditional matrices

Matriz sobre $\mathbb{F}$ = array 2D cuyas entradas son elementos de $\mathbb{F}$. Matriz $m \times n$ = $m$ filas, $n$ columnas. Elemento $i,j$ = fila $i$, columna $j$, notación $A_{i,j}$ o Pythonesa $A[i,j]$.

$$\text{Row } i = [A[i,0], A[i,1], \ldots, A[i,n-1]] \qquad \text{Column } j = [A[0,j], A[1,j], \ldots, A[m-1,j]]$$

**Representación lista-de-filas:** lista $L$ tal que $A[i,j] = L[i][j]$. Matriz $\begin{bmatrix}1&2&3\\10&20&30\end{bmatrix}$ → `[[1,2,3],[10,20,30]]`.

Quiz 4.1.1 (zero matrix 3×4, lista-de-filas):
```python
[[0 for j in range(4)] for i in range(3)]
```

**Representación lista-de-columnas:** lista $L$ tal que $A[i,j] = L[j][i]$ (dualidad fila/columna — todo lo que hacés con columnas lo podés hacer con filas). Misma matriz → `[[1,10],[2,20],[3,30]]`.

Quiz 4.1.2 (matriz 3×4, elemento $i,j = i-j$, lista-de-columnas):
```python
[[i-j for i in range(3)] for j in range(4)]
```
Ojo con el orden: la comprehension externa itera sobre $j$ (columnas), la interna sobre $i$ (filas dentro de cada columna) — al revés de lo intuitivo si pensás "fila primero".

### 4.1.2 The matrix revealed

Igual que un $D$-vector es una función $D \to \mathbb{F}$, una **matriz sobre $\mathbb{F}$** se define como función del producto cartesiano $R \times C \to \mathbb{F}$, donde $R$ = row labels, $C$ = column labels (conjuntos arbitrarios, no solo enteros 0..n-1).

Ejemplo con $R=\{a,b\}$, $C=\{\#,@,?\}$: la matriz es literal un dict `{('a','@'):1, ('a','#'):2, ('a','?'):3, ('b','@'):10, ...}`.

### 4.1.3 Rows, columns, and entries

Fila/columna de una matriz se interpreta como **`Vec`** (mismo tipo que ya usás en `vec.py`):

- Fila `'a'` = `Vec({'@','#','?'}, {'@':1, '#':2, '?':3})`
- Columna `'#'` = `Vec({'a','b'}, {'a':2, 'b':20})`

Notación: $M[r,:]$ o $M_{r,:}$ = fila $r$. $M[:,c]$ o $M_{:,c}$ = columna $c$.

Quiz 4.1.4 (columna `'?'` como `Vec`):
```python
Vec({'a','b'}, {'a':3, 'b':30})
```

### 4.1.4 Representaciones en Python (rowdict / coldict)

**Rowdict:** dict que mapea cada row-label a un `Vec` (la fila entera).
```python
{'a': Vec({'#','@','?'}, {'@':1,'#':2,'?':3}),
 'b': Vec({'#','@','?'}, {'@':10,'#':20,'?':30})}
```

**Coldict:** dict que mapea cada column-label a un `Vec` (la columna entera) — misma dualidad de siempre.

Quiz 4.1.5 (coldict del ejemplo):
```python
{'#': Vec({'a','b'}, {'a':2,'b':20}),
 '@': Vec({'a','b'}, {'a':1,'b':10}),
 '?': Vec({'a','b'}, {'a':3,'b':30})}
```

**Insight clave:** rowdict y coldict son representaciones equivalentes de la misma matriz — no hace falta guardar las dos.

### 4.1.4 Our Python implementation of matrices (p.189-190) — confirmado en libro

Clase `Mat`, análoga a `Vec`, con 2 campos:
- `D` → par `(R, C)` de sets (a diferencia de `Vec` donde `D` es UN solo set)
- `f` → dict que mapea pares `(r,c) ∈ R×C` a valores del campo

Sparsity: entradas con valor 0 no necesitan estar en el dict (igual que `Vec`). Más importante acá porque matrices son $|R|\times|C|$, mucho más grandes que vectores.

**Por qué D es un par y no todo $R\times C$:** guardar el producto cartesiano completo gastaría demasiado espacio en matrices sparse grandes — `D` guarda solo los sets `R` y `C`, `f` guarda solo las entradas no-cero.

```python
class Mat:
    def __init__(self, labels, function):
        self.D = labels
        self.f = function

M = Mat(({'a','b'}, {'@','#','?'}), {('a','@'):1, ('a','#'):2, ('a','?'):3,
                                       ('b','@'):10, ('b','#'):20, ('b','?'):30})
```

**Verificado en `05-Projects/coding-the-matrix`:** crear la instancia funciona igual que el ejemplo. Pero `print(M)` da el `repr` crudo (`Mat({...}, {...})`), NO la tabla bonita `# @ ?` / `a | 1 2 3` que muestra el libro — el libro mismo dice que el pretty-printing con `__str__` viene "eventually", más adelante en el capítulo. Todavía no implementado en este proyecto.

### 4.1.5 Identity matrix (p.190)

$D\times D$ identity matrix: row-labels y col-labels son ambos $D$, entrada $(d,d)=1$ para todo $d\in D$, resto 0. Notación $\mathbb{1}_D$.

```python
def identity(D): return Mat((D, D), {(d, d): 1 for d in D})
```

### 4.1.6 Converting between matrix representations (p.190-191)

```python
def mat2rowdict(A):
    return {r: Vec(A.D[1], {c: A[r, c] for c in A.D[1]}) for r in A.D[0]}

def mat2coldict(A):
    return {c: Vec(A.D[0], {r: A[r, c] for r in A.D[0]}) for c in A.D[1]}
```

Patrón: fila `r` = `Vec` sobre el domain de columnas, evaluando `A[r,c]` para cada `c`. Columna `c` = simétrico.

### 4.1.7 matutil.py (p.191-192)

Provee `identity`, `mat2rowdict`/`mat2coldict` y sus inversas `rowdict2mat`/`coldict2mat`, más `listlist2mat(L)` (conveniente para crear matrices chicas de ejemplo desde lista de listas).

---

## Ver también

- [[Linear-Algebra-Axler-Fundamentals]] — versión formal/rigurosa (Axler)
- [[Linear-Algebra-Basics]] — intuición geométrica (3b1b)
