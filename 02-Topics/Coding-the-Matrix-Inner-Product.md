---
tags: [phase-0, math, linear-algebra, coding-the-matrix, inner-product, orthogonality, projection, machine-learning, gradient-descent]
status: solid
first_learned: 2026-08-07
last_reviewed: 2026-08-08
confidence: 5/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Coding the Matrix — Cap 8: The Inner Product (Klein)

Nota: sigue de [[Coding-the-Matrix-Gaussian-Elimination]]. Este capítulo define length (norm) y perpendicular (orthogonal) en Mathese, y resuelve el *fire engine problem*: encontrar el punto de una línea más cercano a un punto dado.

## 8.1 — El fire engine problem

Casa en b=[2,4], calle es la línea por el origen y v=[6,2]. Preguntas: qué punto de la calle está más cerca de la casa, y cuánto mide esa distancia (¿alcanza la manguera de 3.5 unidades?).

**Computational Problem 8.1.1:** dado v y b, encontrar el punto en {αv : α∈R} más cercano a b.

## 8.1.1 — Norm properties

`||v||` (norm, generaliza "largo") debe cumplir:
- N1: `||v||` es real no-negativo
- N2: `||v|| = 0` sii v es vector cero
- N3: `||αv|| = |α| ||v||`
- N4: `||u+v|| <= ||u|| + ||v||` (desigualdad triangular)

La norm se define vía **inner product**: `||v|| = sqrt(<v,v>)`. No existe forma de definir inner product sobre GF(2) cumpliendo los axiomas — de acá en adelante el libro deja GF(2) de lado.

**Cita:** (*Sección 8.1.1*, p.419-420)

## 8.2 — Inner product para reales = dot product

`<u,v> = u·v`. Propiedades: linealidad en primer argumento (`<u+v,w>=<u,w>+<v,w>`), simetría (`<u,v>=<v,u>`), homogeneidad (`<αu,v>=α<u,v>`).

De esto sale `||v||^2 = suma de v_i^2` — coincide con Pitágoras en R^2 (Ejemplo 8.2.1).

**Cita:** (*Sección 8.2*, p.420-421)

## 8.3 — Orthogonality

*Orthogonal* = Mathese para perpendicular. Se define al revés: se busca la condición que hace que Pitágoras valga para u+v.

**Idea simple:** expandiendo `||u+v||^2 = <u,u> + 2<u,v> + <v,v> = ||u||^2 + 2<u,v> + ||v||^2`, esto solo iguala `||u||^2 + ||v||^2` (Pitágoras exacto) si `<u,v>=0`. Por eso: **u y v son ortogonales ⟺ `<u,v> = 0`**.

**Lemma 8.3.2 (Orthogonality Properties):**
- O1: si u ⊥ v, entonces αu ⊥ αv para cualquier escalar α
- O2: si u ⊥ w y v ⊥ w, entonces (u+v) ⊥ w

**Lemma 8.3.3:** si u ⊥ v, entonces `||αu+βv||^2 = α²||u||² + β²||v||²` (Pitágoras generalizado — los términos cruzados se cancelan por ortogonalidad).

**Cita:** (*Sección 8.3, Lemma 8.3.2-8.3.3*, p.422-423)

### 8.3.2 — Descomposición paralela + ortogonal

**Definición 8.3.6:** para cualquier b y v, se definen `b^||v` (proyección de b a lo largo de v) y `b^⊥v` (proyección de b ortogonal a v) tales que:
1. `b = b^||v + b^⊥v`
2. `b^||v = σv` para algún escalar σ
3. `b^⊥v` es ortogonal a v

**Ejemplo 8.3.7:** en el plano, línea = eje x, v=(1,0), b=(b1,b2). Entonces `b^||v=(b1,0)`, `b^⊥v=(0,b2)` — la proyección "along" agarra la coordenada que coincide con v, la "orthogonal" agarra el resto.

**Caso v=0:** la única `b^||v` posible es el vector cero → `b^⊥v = b`. Consistente porque todo vector es ortogonal al vector cero.

**Cita:** (*Sección 8.3.2, Definición 8.3.6*, p.424)

### 8.3.3 — Fire Engine Lemma

**Lemma 8.3.8:** el punto en Span{v} más cercano a b es `b^||v`, y la distancia es `||b^⊥v||`.

**Por qué (idea de la prueba):** para cualquier otro punto p de la línea, los tres puntos p, `b^||v`, b forman un triángulo rectángulo (`b^||v - p` y `b - b^||v` son ortogonales entre sí, porque `b - b^||v` es ortogonal a v y tanto `b^||v` como p son múltiplos de v). Por Pitágoras, `||b-p||² = ||b^||v - p||² + ||b - b^||v||²`. Si `p ≠ b^||v`, el primer término es positivo → `||b - b^||v|| < ||b - p||`. Nada le gana a `b^||v`.

**Cita:** (*Lemma 8.3.8*, p.425-427)

### 8.3.4 — Cómo calcular σ

De `<b^⊥v, v> = 0` sustituyendo `b^⊥v = b - σv`, se llega a `<b,v> - σ<v,v> = 0`, y despejando:

```
σ = <b,v> / <v,v>
```

Si `||v||=1`, se simplifica a `σ = <b,v>`.

**Beware (floating-point):** si `v` tiene entradas diminutas por error de redondeo, hay que tratarlo como vector cero — convención del libro: `v` es cero si `<v,v> <= 1e-20`.

**Cita:** (*Sección 8.3.4, ecuaciones 8.6-8.8*, p.426-427)

### 8.3.5 — Solución al fire engine problem

Con v=[6,2], b=[2,4]:

```
σ = (v·b)/(v·v) = (6·2 + 2·4)/(6·6 + 2·2) = 20/40 = 1/2
punto más cercano = (1/2)[6,2] = [3,1]
distancia = ||[2,4]-[3,1]|| = ||[-1,3]|| = sqrt(10) ≈ 3.16
```

3.16 < 3.5 → la casa se salva.

Esta noción de "mejor aproximación" (el punto en un subespacio más cercano a un vector dado) reaparece en least-squares/regression, image compression, PCA, latent semantic analysis, compressed sensing.

**Cita:** (*Ejemplo 8.3.14*, p.428)

### 8.3.6 — Outer product y proyección como matriz

El *outer product* de u y v es el producto matriz-matriz `u v^T` (columna × fila = matriz n×n). Sirve para expresar la proyección como producto matriz-vector.

Para v no-cero con `||v||=1`: `π_v(x) = (v·x)v = (v v^T) x`. Como `π_v` es un producto matriz-vector, es automáticamente lineal (Proposition 4.10.2). `v v^T` tiene **rank 1**.

**Eficiencia (Problem 8.3.17):** computar `M·v` directo con la matriz n×n armada cuesta n² multiplicaciones. Factorizando en dos pasos — primero `v^T x` (escalar), después `v·escalar` — cuesta solo 2n. Mismo patrón que "no armar la matriz completa si podés factorizar la operación".

**Cita:** (*Sección 8.3.6*, p.429-430)

## Implementación propia

`05-Projects/coding-the-matrix/src/coding_the_matrix/orthogonalization.py`:
- `project_along(b, v)` — `b^||v`, resuelve el fire engine problem directo
- `project_orthogonal_1(b, v)` — `b^⊥v = b - project_along(b, v)`
- `projection_matrix(v)` — matriz M = outer product `v v^T / <v,v>` tal que `M·x = project_along(x, v)` para todo x

15 tests en `tests/test_orthogonalization.py` (más 3 doctests): ejemplo fire engine exacto del libro, casos borde (v=0, b ya paralelo/ortogonal a v), y propiedades de la matriz de proyección (simétrica, idempotente — `M(Mx)=Mx` —, kernel = ortogonal complement de v, imagen = Span{v}). 130/130 tests del proyecto pasan (excluidos los 4 archivos que dependen de `jinja2`, no instalado — falla preexistente no relacionada).

Decisión de diseño: mismo umbral `1e-20` que el libro para tratar v como vector cero por floating-point roundoff (`ZERO_THRESHOLD` en el módulo).

## Por qué importa para ML/AI

`project_along` ES el least-squares de 1 variable: encontrar el múltiplo escalar de un vector que mejor aproxima a otro. El próximo capítulo generaliza esto de "proyectar sobre 1 vector" a "proyectar sobre el span de varios vectores" — ahí aparece Gram-Schmidt, QR decomposition, y la versión completa de regresión lineal. `projection_matrix` (outer product, rank 1) es además el bloque de construcción de PCA: los componentes principales son proyecciones sobre ejes ortogonales encontrados por eigendecomposition.

## 8.4 — Lab: Machine Learning (WDBC breast cancer)

Aplicación práctica de Cap 8: diagnosticar cáncer de mama a partir de features de imagen usando un classifier lineal entrenado con gradient descent.

### 8.4.1 — El dataset

**Wisconsin Diagnostic Breast Cancer (WDBC).** Por paciente: vector de 30 features (mean, standard error, y "worst" — media de los 3 valores más grandes — de 10 cantidades computadas por núcleo celular: radius, texture, perimeter, area, smoothness, compactness, concavity, concave points, symmetry, fractal dimension). Provisto por el companion site del libro (`resources.codingthematrix.com`), NO se commitea al repo (público, material de curso con restricción de redistribución) — vive en `05-Projects/coding-the-matrix/data/` (gitignored), 300 pacientes en `train.data`, 260 en `validate.data`.

**Cita:** (*Sección 8.4.1*, p.430-431)

### 8.4.2-8.4.3 — Hypothesis class y classifier

Un classifier se elige de un conjunto de candidatos posibles (**hypothesis class**). Acá: funciones lineales `h(y) = w·y`, donde w (**hypothesis vector**) tiene el mismo domain D que los features — toda función lineal de R^D a R se puede escribir como dot product contra algún vector fijo, así que "elegir h" ⟺ "elegir w". El classifier final: `C(y) = +1 si h(y)>=0 (malignant), -1 si h(y)<0 (benign)`. Geometría: `w·y=0` define un hiperplano por el origen en R^D que separa el espacio en dos mitades.

`signum(u)`: convierte cada entrada de un vector a su signo (+1/-1), elementwise — building block, no confundir con el dot product.

`fraction_wrong(A, b, w)`: fracción de pacientes donde `signum(A*w)` difiere de `b`. Vectorizado: `A*w` da todos los dot products de una, sin loop.

**Cita:** (*Sección 8.4.2-8.4.3, Tasks 8.4.2-8.4.3*, p.431-432)

### 8.4.4 — Loss function

`fraction_wrong` es difícil de minimizar directamente (función escalonada, no diferenciable). Se usa en cambio el **squared error**: para cada ejemplo, `(h(a_i)-b_i)^2`. Suma total = `L(x) = (a1·x-b1)^2+...+(am·x-bm)^2`.

**Dualidad (observación propia de la sesión):** L se puede escribir de dos formas equivalentes — suma de dot products escalares al cuadrado, o `||Aw-b||^2` (norma al cuadrado de un vector, resultado de matrix-vector mult). Son la misma cosa porque `||v||^2 = suma de v_i^2` (Cap 8.2). El objetivo es minimizar `||Aw-b||^2` — el capítulo de Orthogonalization resuelve esto directo con proyección (generalización de `project_along` a varios vectores, sin gradient descent).

`loss(A, b, w) = residual * residual` donde `residual = A*w - b` — el dot product de un vector consigo mismo YA es la suma de cuadrados, sin loop ni suma explícita.

Por qué cuadrado y no valor absoluto: elimina negativos, penaliza más los errores grandes, y es diferenciable suave (sin esquinas) — necesario para gradient descent. Nombre en PyTorch: **MSE** (`nn.MSELoss`).

**Cita:** (*Sección 8.4.4, Task 8.4.4*, p.432-433)

### 8.4.5 — Hill-climbing

Heurística genérica para encontrar el mínimo de una función: mantener w, iterar `w := w + change` (un vector chico que depende de dónde estás parado). Analogía de terreno: cada w es un punto, el valor de la función es la altitud. `L(w)` es convexa (forma de tazón, un solo mínimo) — hill-climbing funciona bien acá. En terrenos complicados (varios valles) puede quedar atrapado en un **mínimo local** en vez del **mínimo global** — inevitable porque encontrar el mínimo global exacto es computacionalmente intratable en general.

**Cita:** (*Sección 8.4.5*, p.433-434)

### 8.4.6 — Gradient

Para una función lineal, la pendiente es constante — la dirección de bajada se calcula una sola vez. Para una función no-lineal (como L), la pendiente depende de dónde estás parado, hay que recalcular después de cada paso.

**Definición 8.4.6:** el **gradient** de f, `∇f`, es el vector de derivadas parciales `[∂f/∂x1,...,∂f/∂xn]` — da un VECTOR, no un número. `∇f(w)` apunta en la dirección de steepest ascent desde w; `-∇f(w)` es steepest descent.

**Regla de la cadena aplicada** (Ejemplo 8.4.8): para `f(x)=(a·x-b)^2`, `∂f/∂xj = 2(a·x-b)*aj` — derivada de la capa externa (`2*(a·x-b)`, regla de potencia) por la derivada de la capa interna (`aj`, porque en `a·x = a1x1+...+ajxj+...`, solo el término `aj*xj` depende de xj). `aj` es simplemente la entrada j del vector a — un escalar, no el vector completo.

Aplicado a L completa: `∇L(w) = suma_i [2(ai·w-bi)*ai]` (ecuación 8.9) — combinación lineal de los vectores training-example `ai`, con coeficientes `2*residual_i`.

`find_grad(A, b, w) = 2 * (A.transpose() * residual)`. Por qué el transpose reemplaza el loop: `matrix_vector_mul` ya suma sobre el eje compartido (columnas de la matriz) — transponer pone "pacientes" como ese eje, así el resultado acumula automáticamente `residual_i * a_i` para cada paciente sin loop explícito escrito a mano.

**Historia (research propia):** gradient descent no fue inventado para ML — Cauchy lo formuló en 1847 para ecuaciones no-lineales generales. Ver [[gradient-descent-history-origin]] para la investigación completa.

**Cita:** (*Sección 8.4.6, Task 8.4.9*, p.434-436)

### 8.4.7 — Gradient descent y step size

Algoritmo: `w := w - σ*∇L(w)` repetido T veces, donde σ (**step size**) es un escalar chico. Por qué chico: el gradiente es información LOCAL (válida solo cerca de donde estás parado) — un paso grande puede pasarse del mínimo (**overshoot**) y hasta hacer que la loss explote en vez de bajar.

**Demo numérica propia** (dataset toy 3 pacientes, w=[1,1], loss=5.25): `sigma=0.01 → loss=3.70` (mejora); `sigma=0.1 → loss=6.93` (empeora); `sigma=0.5 → loss=395.83`; `sigma=2.0 → loss=7300` (diverge). Confirmado también en datos reales: `sigma=1e-9` converge, `sigma=2e-9` diverge a `nan`.

`gradient_descent_step(A,b,w,sigma) = w - sigma*find_grad(A,b,w)`. `gradient_descent(A,b,w,sigma,T)` repite el step T veces.

**Cita:** (*Sección 8.4.7, Tasks 8.4.10-8.4.11*, p.436-437)

### 8.4.12-8.4.13 — Entrenamiento real y generalización

Corrida sobre `train.data` (300 pacientes, 30 features), w0=vector cero, sigma=1e-9, T=10000:
```
inicio:  loss=1,461,169,191   fraction_wrong=0.51
final:   train loss=174.1     fraction_wrong=0.16
         validate loss=135.1  fraction_wrong=0.054
```
`sigma=2e-9` (el doble) diverge a `nan` — confirma la lección de overshoot en 30 dimensiones reales, no solo en el ejemplo toy.

**Resultado llamativo:** el error en `validate.data` (5.4%) fue MENOR que en `train.data` (16%) — al revés de la intuición de overfitting clásico. Explicación más probable: `validate.data` es más chico (260 vs 300 pacientes), el ruido de muestreo pesa más en sets chicos; y el modelo no llegó a converger del todo (T=30000 mejora poco sobre T=10000), así que no hay señal de haber memorizado el training set.

**Cita:** (*Tasks 8.4.12-8.4.13*, p.437)

## Implementación propia

`05-Projects/coding-the-matrix/src/coding_the_matrix/orthogonalization.py`:
- `project_along(b, v)` — `b^||v`, resuelve el fire engine problem directo
- `project_orthogonal_1(b, v)` — `b^⊥v = b - project_along(b, v)`
- `projection_matrix(v)` — matriz M = outer product `v v^T / <v,v>` tal que `M·x = project_along(x, v)` para todo x

15 tests en `tests/test_orthogonalization.py` (más 3 doctests): ejemplo fire engine exacto del libro, casos borde (v=0, b ya paralelo/ortogonal a v), y propiedades de la matriz de proyección (simétrica, idempotente — `M(Mx)=Mx` —, kernel = ortogonal complement de v, imagen = Span{v}).

`05-Projects/coding-the-matrix/src/coding_the_matrix/ml_lab.py`:
- `signum(u)`, `fraction_wrong(A,b,w)`, `loss(A,b,w)`, `find_grad(A,b,w)`, `gradient_descent_step(A,b,w,sigma)`, `gradient_descent(A,b,w,sigma,T)`
- `read_training_data(fname)` — parser propio del formato WDBC (CSV: ID, diagnosis M/B, 30 features en bloques mean/stderr/worst), escrito desde cero replicando el contrato del libro — no se copió el `cancer_data.py` del sitio del curso (mismo motivo de copyright que el dataset)

22 tests en `tests/test_ml_lab.py` (más 4 doctests), incluyendo 2 tests condicionales que corren sobre el dataset real (`train.data`, se saltan si el archivo no está presente localmente). 165/165 tests del proyecto pasan (jinja2 se instaló vía `uv sync`, destrabando también los tests de `viz_html` que antes se ignoraban; se corrigió además un bug preexistente de encoding en `viz_html.py` — `write_text` sin `encoding="utf-8"` fallaba en Windows/cp1252 con caracteres como `→`).

`05-Projects/coding-the-matrix/src/coding_the_matrix/visualize_ml_lab.py` — visualizador interactivo matplotlib (mismo patrón de `visualize_gaussian.py`, navegación con flechas): 3 paneles — loss curve y fraction_wrong curve (train vs validate, 30 features reales) revelados progresivamente, más un panel de frontera de decisión 2D (radius vs texture) rotando en vivo a medida que gradient descent entrena, con scatter real de pacientes coloreado por diagnóstico. Correr: `cd 05-Projects/coding-the-matrix && uv run python -m coding_the_matrix.visualize_ml_lab`.

## Doubts Resolved

- [[linear-classifier-perceptron-pytorch]] — el classifier `signo(w·y)` de este lab es exactamente el perceptrón clásico; cómo lo implementa PyTorch (`torch.sign`, `nn.Linear`, autograd vs derivación manual)
- [[gradient-descent-history-origin]] — de dónde viene gradient descent (Cauchy 1847), por qué terminó siendo el algoritmo de entrenamiento de IA

## Ver también

- [[Coding-the-Matrix-Gaussian-Elimination]] — capítulo anterior
- [[Linear-Algebra-Basics]] — dot product / embeddings desde la perspectiva 3Blue1Brown
