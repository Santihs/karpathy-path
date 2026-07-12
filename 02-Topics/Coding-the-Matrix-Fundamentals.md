---
tags: [phase-0, math, linear-algebra, coding-the-matrix]
status: learning
first_learned: 2026-07-01
last_reviewed: 2026-07-12
confidence: 5/5
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

**Pendiente de implementar en el proyecto** (`05-Projects/coding-the-matrix`): `identity`, `mat2rowdict`, `mat2coldict` en `mat.py`; módulo `matutil.py` nuevo con `rowdict2mat`/`coldict2mat`/`listlist2mat`.

---

## 6. Cap 4.2 — Column space and row space (p.192)

**Idea:** una matriz empaqueta un montón de vectores, y hay 2 formas de leerla como tal: como bunch de columnas, o bunch de filas. Cada lectura genera un espacio vectorial propio:

- **Col space** ($\text{Col } M$) = span de las columnas de $M$.
- **Row space** ($\text{Row } M$) = span de las filas de $M$.

**Ejemplo (4.2.2):** $M = \begin{bmatrix}1&2&3\\10&20&30\end{bmatrix}$.
- Col space = Span{[1,10], [2,20], [3,30]} = Span{[1,10]} solamente — las otras 2 columnas son múltiplos escalares de la primera, no aportan dirección nueva.
- Row space = Span{[1,2,3], [10,20,30]} = Span{[1,2,3]} — misma razón, fila 2 = 10× fila 1.

**Por qué importa:** el tamaño real (dimensión) de estos spans es el **rank** de la matriz — acá rank 1, aunque la matriz sea 2×3.

---

## 7. Cap 4.3 — Matrices as vectors (p.193)

**Idea clave:** una matriz $R\times C$ sobre $\mathbb{F}$ es, por definición, una función $R\times C \to \mathbb{F}$ — exactamente la misma forma que un $D$-vector es función $D\to\mathbb{F}$. Solo cambia qué es el domain: para `Vec` es un set plano, para `Mat` es un producto cartesiano de 2 sets. Estructuralmente es EL MISMO objeto (mismo tipo de dict `{label: valor}`), no un objeto anidado.

**mat2vec (Quiz 4.3.1):** aplana un `Mat` a un `Vec` sin transformar nada — domain nuevo es el set de pares `(r,c)`, y el storage (`f`) se reusa tal cual porque las keys de `Mat.f` YA son tuplas `(r,c)`.

```python
def mat2vec(M):
    return Vec({(r,s) for r in M.D[0] for s in M.D[1]}, M.f)
```

**Analogía:** igual que `.view(-1)`/`.flatten()` en un tensor PyTorch — mismo storage/memoria, solo cambia el "shape" con que lo interpretás. Cero copia.

**Contraste con `mat2rowdict`:** ESE sí hace trabajo real (arma un `Vec` nuevo por cada fila, iterando columnas) — resultado es un dict `row_label -> Vec`, una estructura de 2 niveles genuina. `mat2vec` es la operación opuesta: colapsar a 1 nivel.

**Nota:** el libro dice que no vamos a necesitar `mat2vec` en la práctica porque `Mat` va a incluir sus propias operaciones de vector (`+`, escalar-mult) directamente — ya implementadas en `mat.py` (`add`, `scalar_mul`).

---

## 8. Cap 4.4 — Transpose (p.194)

**Definición (4.4.1):** transponer invierte filas y columnas. Si $M$ es $P\times Q$, $M^T$ es $Q\times P$, con regla $(M^T)_{j,i} = M_{i,j}$ para todo $i\in P, j\in Q$ — la entrada que vivía en (fila $i$, col $j$) pasa a (fila $j$, col $i$).

**Ejemplo (Quiz 4.4.2):** $M$ 3×2 con filas `#,@,?` y columnas `a,b`:
```
        a    b
   #  [ 2   20 ]
   @  [ 1   10 ]
   ?  [ 3   30 ]
```
$M^T$ (2×3) — se invierte:
```
       #   @   ?
   a [ 2   1   3 ]
   b [20  10  30 ]
```
Chequeo: $M[(@,a)]=1$ → $M^T[(a,@)]=1$. Mismo valor, índices invertidos.

**Implementación (ya en `mat.py:85-95`, coincide con la respuesta del libro):**
```python
def transpose(M):
    return Mat((M.D[1], M.D[0]), {(c,r): v for (r,c),v in M.f.items()})
```
Analogía: como transponer una tabla de Excel — "columna A, fila 3" pasa a "columna 3, fila A". El valor no cambia, solo el eje. Puro reetiquetado de la key, sin cálculo.

**Matriz simétrica:** $M$ es simétrica si $M^T = M$. Ejemplo: $\begin{bmatrix}1&2\\2&4\end{bmatrix}$ es simétrica ($M[0,1]=M[1,0]=2$); $\begin{bmatrix}1&2\\3&4\end{bmatrix}$ no lo es.

---

## 9. Cap 4.5 — Matrix-vector y vector-matrix multiplication (linear combinations) (p.194-200)

Hay 2 direcciones de multiplicar matriz×vector, NO son intercambiables:

### 4.5.1 — matrix-vector (`M*v`)

`v` debe ser un **C-vector** (domain = columnas de M). Resultado = combinación lineal de las COLUMNAS de M, pesadas por las entradas de v:

$$M*v = \sum_{c} v[c]\cdot(\text{columna } c \text{ de } M)$$

Ejemplo (4.5.2): `M=[[1,2,3],[10,20,30]]`, `v=[7,0,4]`:
```
7*[1,10] + 0*[2,20] + 4*[3,30] = [7,70]+[0,0]+[12,120] = [19,190]
```
Ilegal si `len(v) != cantidad de columnas` (4.5.3: M 2×3, v de 2 entradas → ilegal).

### 4.5.2 — vector-matrix (`v*M`)

`v` debe ser un **R-vector** (domain = filas de M). Resultado = combinación lineal de las FILAS de M, pesadas por v:

$$v*M = \sum_{r} v[r]\cdot(\text{fila } r \text{ de } M)$$

Ejemplo (4.5.7): `[3,4]*[[1,2,3],[10,20,30]] = 3*[1,2,3]+4*[10,20,30] = [3,6,9]+[40,80,120] = [43,86,129]`.

Ilegal si `len(v) != cantidad de filas` (4.5.8: M 2×3, v de 3 entradas — matchea columnas no filas → ilegal, regla espejo de 4.5.3).

**Regla general (una sola, aplicada 2 veces):** es el mismo shape-rule de matrix_matrix_mul, `(m×n)·(n×p)=(m×p)` — un vector es matriz con una dimensión=1 (columna=n×1, fila=1×n).

**Remark 4.5.9 — por qué NO implementar `v*M` como `transpose(M)*v`:** matemáticamente es válido (fila de M = columna de M^T), pero transpose crea una matriz nueva completa — ineficiente si M es grande. Mejor calcular directo (ya hecho en `vector_matrix_mul`, `mat.py`).

**Ejemplo real 4.5.10 — JunkCo:** tabla `M` = productos(filas)×recursos(columnas). Vector `u` = cantidad producida de cada producto. `u*M` = consumo total por recurso (combinación lineal de filas, pesada por cantidades). Mismo patrón que "pesos×features" en ML.

```python
rowdict = {'gnome':v_gnome, 'hoop':v_hoop, 'slinky':v_slinky, 'putty':v_putty, 'shooter':v_shooter}
M = rowdict2mat(rowdict)
u = Vec(R, {'putty':133,'gnome':240,'slinky':150,'hoop':55,'shooter':90})
u*M  # -> metal:51.0 concrete:312.0 plastic:215.4 water:373.1 electricity:356.0
```

### 4.5.3 — formular "expresar vector como combinación lineal" como ecuación matriz-vector

Idea: en vez de CALCULAR una combinación lineal, plantear la ecuación al revés — "qué pesos necesito para llegar a este resultado".

- **Industrial espionage (4.5.11):** observás consumo total `b`, conocés la receta `M`, incógnita `x` = cantidad producida. Ecuación: `x*M = b`.
- **Lights Out (4.5.12):** `button_vectors(n)` arma dict `botón(i,j) -> Vec` (efecto cruz: prende/apaga sí mismo + 4 vecinos, GF(2)). `B = coldict2mat(button_vectors(n))` (botones como COLUMNAS). Estado inicial `s`, incógnita `x` (qué botones apretar). Ecuación: `B*x = s`.

Ambos ejemplos son la misma estructura: `matriz_conocida * incógnita = observado`.

### 4.5.4 — Computational Problem 4.5.13 (solve matrix-vector equation)

Spec formal: input `A` (Mat), `b` (R-vector) → output `u` (C-vector) tal que `A*u = b`.

**Truco de la transpuesta:** un algoritmo para `A*u=b` también resuelve `x*A=b` (vector-matrix) transponiendo A primero y llamando `solve(A.transpose(), b)` — porque `x*A = b` ⟺ `A^T*x = b` (misma suma, identidad matemática, no coincidencia). Evita programar 2 algoritmos.

**Ejemplo 4.5.15 — resolviendo el espionaje al revés:** dado `b` (consumo observado) y `M` (receta), `solve(M.transpose(), b)` da `x` (producción deducida): `putty:133, gnome:240, slinky:150, hoop:55, shooter:90`.

**Verificar con residual:** `residual = b - solution*M`. Si fuera exacto, residual = vector cero. Con floats nunca exacto — se chequea `residual*residual` (dot-product consigo mismo = suma de cuadrados = "qué tan lejos de cero en total"). Valor `~1e-25` = prácticamente cero para fines prácticos. Mismo patrón que MSE en ML.

**Caveat importante:** residual≈0 NO garantiza que sea la ÚNICA solución — puede haber múltiples soluciones (conecta con null space/rank, capítulos posteriores). El módulo `solver` (con `solve()`) es referencia provista por el libro para capítulos futuros de eliminación gaussiana — no se re-implementa en este proyecto todavía.

---

## 10. Cap 4.6 — Matrix-vector multiplication en términos de dot-products (p.201-206)

Definición EQUIVALENTE a la de 4.5 (linear combinations) — mismo resultado, distinta forma de pensarlo/calcularlo.

### 4.6.1 — Definiciones

- `M*u` (matrix-vector): resultado[r] = dot-product(fila r de M, u). Ya implementado así en tu código (`matrix_vector_mul`).
- `u*M` (vector-matrix): resultado[c] = dot-product(u, columna c de M). Ya implementado (`vector_matrix_mul`).

Ejemplo 4.6.2: `[[1,2],[3,4],[10,0]] * [3,-1]`. Cada fila hace dot-product con `[3,-1]`:
```
[1,2]·[3,-1] = 1*3+2*(-1) = 1
[3,4]·[3,-1] = 3*3+4*(-1) = 5
[10,0]·[3,-1] = 10*3+0*(-1) = 30
```
Resultado `[1,5,30]`. Validado en `tests/test_mat.py::test_matrix_vector_mul_dot_product_book_example_4_6_2`.

### 4.6.2 — Aplicaciones (downsampling, blur, linear filters)

**Downsampling (4.6.4):** reducir resolución de imagen. Cada pixel de salida = promedio de un bloque de pixels de entrada. Promedio = dot-product con pesos iguales (`1/16` para bloque 4×4). Cada FILA de M tiene 16 entradas no-cero (una por pixel del bloque), resto 0. `v = M*u` calcula toda la imagen chica de una.

**Blur (4.6.5):** mismo mecanismo, pero input/output mismo tamaño — filas que blurrean (promedio de vecinos) mezcladas con filas que copian intacto (fila = vector identidad). Nunca se construye la matriz de verdad en la práctica — el valor es conceptual (Cap 10 explica cómo aplicar la transformación rápido sin construirla).

**Simple average vs Gaussian blur:** ambos son "promedio de vecinos" con pesos distintos — simple average pesa todo igual (artefactos visuales), Gaussian pesa más cerca del centro, cae con la distancia. Cualquier transformación `M*v` de este tipo se llama **linear filter** (conecta con 2.9.3).

**Conexión ML:** un kernel de convolución (conv2d, average pooling) ES un linear filter — mismo mecanismo, distintos pesos según el kernel.

### 4.6.6 — Needle-in-haystack como matrix-vector (circulant matrix)

Buscar `[0,1,-1]` en `[0,0,-1,2,3,-1,0,1,-1,-1]`: en vez de 10 dot-products sueltos (uno por posición), 1 matriz `M` (10 filas) donde fila `i` = needle colocado empezando en columna `i`, con **wrap-around** (needle que se pasa del final vuelve a empezar por columna 0 — como cinta circular).

```python
M = Mat((D,D), {(i, (i+k)%n): val for i in range(n) for k,val in enumerate(needle)})
result = M * haystack  # = [1,-3,-1,4,-1,-1,2,0,-1,0]
```

**Match real:** posición 6 (`haystack[6:9] == needle` exacto) da 2 — el TECHO teórico para este needle (el 0 inicial limita el máximo posible a 0+1+1=2). Posición 3 da 4 (más alto numéricamente) pero es coincidencia — no hay match estructural ahí. Lección: número más alto ≠ mejor match cuando el patrón tiene ceros.

**Por qué wrap-around importa:** esta estructura (cada fila = la anterior corrida 1, con wraparound) se llama **matriz circulante** — habilita el algoritmo FFT (Fast Fourier Transform, Cap 10) para calcular `M*v` en `O(n log n)` en vez de `O(n²)`. Conecta con cross-correlation/conv1d en señales y ML.

Validado en `tests/test_mat.py::test_needle_in_haystack_as_matrix_vector_book_example_4_6_6`.

### 4.6.3 — Sistema de ecuaciones lineales como ecuación matriz-vector

Un sistema `a_1·x=β_1, a_2·x=β_2, ..., a_m·x=β_m` es EXACTAMENTE `A*x=b`, donde filas de A = los `a_i`, y b = `[β_1,...,β_m]`. Puro empaquetado usando la definición dot-product de 4.6.1.

**Ejemplo 4.6.7 — corriente de hardware (sensor node):** 4 componentes (radio, sensor, memory, CPU), corriente de cada uno = incógnita. 5 períodos de prueba, cada uno da 1 ecuación (`duration_i · rate = consumo_observado_i`). Empaquetado:
```python
A = rowdict2mat([v0,v1,v2,v3,v4])  # cada v_i (duración) = 1 fila
b = Vec({0,1,2,3,4}, {0:140, 1:170, 2:60, 3:170, 4:250})
rate = solve(A, b)  # -> radio:500, sensor:250, memory:100, CPU:300
```
`rowdict2mat` (implementado hoy) acepta también LISTA (no solo dict) — índice de lista se vuelve row label, uso exacto de este ejemplo.

**Reformulación general:** "resolver sistema lineal" (2.9.12) → "resolver A*x=b" (4.5.13, ya visto). "¿Cuántas soluciones sobre GF(2)?" (2.9.18, esquema de autenticación) → misma pregunta en lenguaje matricial. De acá en adelante el libro resuelve todo en términos de matrices.

Validado en `tests/test_mat.py::test_sensor_current_system_as_matrix_vector_book_example_4_6_7` (verifica que la solución dada por el libro satisface `A*rate == b` — no hay módulo `solver` implementado en este proyecto todavía, es referencia de capítulos futuros de eliminación gaussiana).

---

## 11. Cap 4.6.4 — Triangular systems and triangular matrices (p.206-208) + implementación

### 4.6.8 — Sistema triangular como A*x=b (conexión con Cap 2.11)

El sistema que ya resolvés con `triangular_solve_n` (backward substitution) es literalmente `A*x=b` cuando `A` tiene forma triangular (cada fila "abre" una columna nueva de ceros hacia abajo).

### 4.6.9/4.6.10 — Qué es "triangular" formalmente

Matriz tradicional (índices enteros): upper-triangular si `A[i,j]=0` para `i>j`. Pero tus `Mat` tienen domain = SETS arbitrarios (sin orden natural) — no existe "i>j" sin definir un orden explícito. Por eso Klein generaliza: dadas listas `L_R` (orden de filas elegido) y `L_C` (orden de columnas elegido), `A` es triangular respecto a esas listas si `A[L_R[i], L_C[j]] = 0` para `j > i`.

### 4.6.11 — Reordenar revela estructura oculta

Una matriz puede NO verse triangular en su orden por defecto (alfabético) pero SÍ serlo con otro orden de filas/columnas. Ejemplo del libro (`{a,b,c}×{#,@,?}`):

```
orden alfabético:        orden [b,a,c] / [@,?,#]:
   #  ?  @                  @  ?  #
a  2  3  0               b 10 30 20
b 20 30 10               a  0  3  2
c 35  0  0                c  0  0 35
```

Mismos datos exactos (`A.f` no cambia una sola celda) — el "triángulo" estaba ahí escondido, solo visible eligiendo el orden correcto. Mismo principio que 4.3 (mat2vec): reordenar/reinterpretar ≠ transformar datos.

### Implementación en el proyecto (`mat.py`)

- **`to_str(M)` / `Mat.__str__`**: pretty-print tipo tabla, orden alfabético automático (headers + separador + filas, right-justified al ancho más largo). Doctest + tests en `test_mat.py`.
- **`pp(M, L_R, L_C)` / `Mat.pp()`**: mismo formato de tabla (comparten helper interno `_table`, sin duplicar lógica), pero con el orden de filas/columnas QUE VOS elijas — revela triangularidad oculta. `pp(M, orden_alfabético) == to_str(M)`, validado en test.
- **`find_triangular_order(M)`** (Problem 4.6.12): dado `M`, ENCUENTRA `(L_R, L_C)` que la hagan triangular, o `None` si no existe / si M no es cuadrada. Implementación: fuerza bruta sobre `itertools.permutations` de filas × columnas — `O(n!²)`, válido solo para matrices chicas (las del libro). Devuelve el primer orden válido encontrado.

### Bug real encontrado documentando esto (vale la pena recordarlo)

Al escribir el test copiando la matriz del libro a mano, transcribí mal 2 valores (`a@` y `a#` invertidos) — el test lo detectó de inmediato al fallar contra la propiedad matemática real (`i>j → 0`), no contra un string hardcodeado. Lección: testear la PROPIEDAD (triangularidad real), no solo "se ve como el libro dice" — así un error de transcripción no pasa desapercibido. Ver `tests/test_mat.py::test_pp_reveals_hidden_triangular_structure_book_example_4_6_11`.

### Encontrar Y resolver (Problem 4.6.12 completo, end-to-end)

`find_triangular_order` encuentra el orden; `triangular_solve` (ya implementado, Cap 2.11) lo USA para resolver de verdad:

```python
L_R, L_C = find_triangular_order(A)
rowlist = [A.mat2rowdict()[r] for r in L_R]   # filas, reordenadas
x = triangular_solve(rowlist, L_C, b)          # resuelve con backward substitution
```

Test: `tests/test_mat.py::test_find_order_then_solve_the_3x3_system` — con `b=[60,5,35]` (orden `L_R=[b,a,c]`) da `x={@:1,?:1,#:1}` (elegido a propósito para verificar a mano). Backward substitution paso a paso (dot-products contra la solución parcial):

```
fila_c = [@:0, ?:0, #:35], x_parcial={}          -> x[#] = (35 - 0)/35 = 1
fila_a = [@:0, ?:3, #:2],  x_parcial={#:1}       -> x[?] = (5 - 2)/3 = 1
fila_b = [@:10,?:30,#:20], x_parcial={#:1,?:1}   -> x[@] = (60 - 50)/10 = 1
```

Cada dot-product usa `x_parcial` con las posiciones no resueltas todavía en 0 IMPLÍCITO (sparse `Vec`) — por eso `coef*0=0` "ignora" automáticamente lo que falta resolver, sin lógica especial (mismo mecanismo que ya tenías documentado para `triangular_solve_n`).

### Por qué fuerza bruta no escala — el algoritmo real (Dulmage-Mendelsohn)

`O(n!²)` es inviable para matrices reales (n=20 ya es ~6×10^36 combinaciones). El algoritmo real usado en solvers dispersos (scipy, MATLAB `dmperm`) es la **Dulmage-Mendelsohn decomposition**, en 3 pasos de teoría de grafos:

1. **Matching bipartito máximo**: pensar filas y columnas como 2 grupos de nodos, arista si `M[r,c]!=0`. Buscar el emparejamiento máximo fila↔columna (algoritmo tipo Hopcroft-Karp) — da los candidatos a pivote diagonal, sin probar todas las combinaciones.
2. **Strongly Connected Components (Tarjan)** sobre el grafo de dependencias entre esos pivotes: si hay CICLO (A depende de B y B depende de A), esos nodos forman un bloque irreducible — nunca se puede triangularizar puro ahí, hace falta eliminación gaussiana normal dentro del bloque.
3. **Topological sort** de los bloques (ya sin ciclos entre ellos) → da el orden final.

Resultado: **block-triangular form** en tiempo polinomial (~`O(filas × entradas no-cero)`), no factorial — detecta también matemáticamente cuándo NO se puede triangularizar puro (bloques cíclicos), en vez de agotar combinaciones. **No implementado en este proyecto** — queda documentado como referencia conceptual para cuando se retome con más profundidad en grafos.

## 12. Cap 4.6.5 — Propiedades algebraicas de matrix-vector mult (p.208) — CIERRE Cap 4.6

**Proposición 4.6.13:** para `M` matriz `R×C`:
- **Homogeneidad:** `M*(αv) = α*(M*v)`.
- **Distributividad:** `M*(u+v) = M*u + M*v`.

**Técnica de prueba (la parte que importa):** para probar que 2 vectores son iguales, alcanza con probarlo **entrada por entrada** — reduce "igualdad de vectores" a una afirmación escalar, mucho más simple. Con la definición dot-product (4.6.1):

```
entrada r del lado izq = dot(fila_r de M, αv)        entrada r del lado izq = dot(fila_r de M, u+v)
entrada r del lado der = α * dot(fila_r de M, v)      entrada r del lado der = dot(fila_r de M,u) + dot(fila_r de M,v)
```

Ambas parejas son iguales por las propiedades YA probadas del dot-product suelto (homogeneidad y distributividad — las mismas que ya estaban en el quiz bank de dot-product, `(αu)·v=α(u·v)` y `(u+v)·w=u·w+v·w`). El libro no re-demuestra esas propiedades — las REUSA, escalando de "un dot-product" a "una matriz entera de dot-products". Patrón de construcción: cada capa nueva se apoya en la anterior ya demostrada, sin reinventar.

**Problem 4.6.14** (resuelto en sesión, Socrático): probar Equation 4.4 (distributividad) siguiendo el mismo patrón que 4.3 — se resolvió correctamente identificando que había que invocar la distributividad del dot-product ya conocida.

**Cierre Cap 4.6:** con esto, Cap 4 completo (4.1-4.6) queda documentado + implementado + testeado (66 tests, `05-Projects/coding-the-matrix`).

---

## Ver también

- [[Linear-Algebra-Axler-Fundamentals]] — versión formal/rigurosa (Axler)
- [[Linear-Algebra-Basics]] — intuición geométrica (3b1b)
