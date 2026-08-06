---
tags: [phase-0, math, linear-algebra]
status: learning
first_learned: 2026-06-26
last_reviewed: 2026-08-05
confidence: 3/5
---

# Linear Algebra Basics

Source: 3Blue1Brown — Essence of Linear Algebra, chapters 1–3 (2026-06-26)

---

## My Notes (ch. 1–3)

### Vectores — 3 definiciones

- **Math (física)**: flechas en el espacio — el origen siempre es el mismo
- **CS**: lista ordenada de números — el orden importa (ej. `[2, 5, 5]` en 1D, 2D, etc.)
- **Matemático puro**: cualquier cosa que puedas sumar con otro vector y multiplicar por un escalar

### 2 Operaciones fundamentales

**Suma de vectores** `v + w`: no es solo extender la suma de números — geométricamente es poner un vector al final del otro. El resultado es la diagonal del paralelogramo formado.

**Multiplicación por escalar** (`2v`): estira el vector. Este proceso se llama *escalar* un vector. Si el escalar es negativo, lo voltea.

### Span y vectores base

- Los vectores base î y ĵ son los escalares unitarios de los ejes x e y
- Escalamos î y ĵ para alcanzar cualquier punto del espacio
- Si î y ĵ están **alineados** (paralelos), solo generan una línea recta — perdemos una dimensión
- Si son **linealmente independientes**, su *span* cubre todo el espacio 2D
- En 3D: dos vectores generan un plano; añadir un tercer vector independiente permite alcanzar cualquier punto del espacio 3D

### Transformaciones Lineales y Matrices

- Una transformación = función = `f(x)` — toma un vector de entrada y produce uno de salida
- **2 propiedades que definen "lineal"**:
  1. Las líneas deben seguir siendo líneas rectas (no curvas)
  2. El origen debe permanecer en su lugar
- La matriz **registra** la transformación: te dice a dónde va a parar cada punto del espacio
- Para saber a dónde se mueve cualquier vector, solo necesitas saber a dónde van los vectores base î y ĵ

$$\begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = x\begin{bmatrix} a \\ c \end{bmatrix} + y\begin{bmatrix} b \\ d \end{bmatrix}$$

- **Columna 1** = dónde termina î después de la transformación
- **Columna 2** = dónde termina ĵ después de la transformación

---

## Quiz session — 2026-06-26

**Q: ¿Cuáles son las 3 definiciones de vector? ¿Cuál es la más útil?**
- Tu respuesta: física (flechas con origen fijo), CS (orden importa), matemático (suma y escala)
- Corrección: correcto. La más útil para intuición geométrica es la de **flecha en el espacio con origen fijo**.

**Q: ¿Qué hace una transformación lineal al espacio? ¿Cuáles son sus 2 restricciones?**
- Tu respuesta: las líneas siguen siendo líneas, el origen se queda en su lugar
- Corrección: exacto, sin cambios.

**Q: ¿Qué representan las columnas de una matriz 2×2?**
- Tu respuesta: los vectores que describen cómo se deforma el espacio, cada columna son 2 vectores
- Corrección: más preciso — cada columna es **a dónde va a parar un vector base** (î o ĵ). Como cualquier vector es combinación lineal de los vectores base, saber a dónde van los dos base te dice a dónde va todo.

---

## Formulas de referencia rápida

**Vector como combinación lineal de base:**
$$\vec{v} = x\hat{i} + y\hat{j} = x\begin{bmatrix}1\\0\end{bmatrix} + y\begin{bmatrix}0\\1\end{bmatrix}$$

**Suma de vectores:**
$$\vec{v} + \vec{w} = \begin{bmatrix}v_1\\v_2\end{bmatrix} + \begin{bmatrix}w_1\\w_2\end{bmatrix} = \begin{bmatrix}v_1+w_1\\v_2+w_2\end{bmatrix}$$

**Escalado de un vector:**
$$c\vec{v} = c\begin{bmatrix}v_1\\v_2\end{bmatrix} = \begin{bmatrix}cv_1\\cv_2\end{bmatrix}$$

**Transformación lineal (matriz × vector):**
$$A\vec{v} = \begin{bmatrix}a & b\\c & d\end{bmatrix}\begin{bmatrix}x\\y\end{bmatrix} = x\begin{bmatrix}a\\c\end{bmatrix} + y\begin{bmatrix}b\\d\end{bmatrix} = \begin{bmatrix}ax+by\\cx+dy\end{bmatrix}$$

**Composición de transformaciones (matrices):**
$$M_2(M_1\vec{v}) = (M_2 M_1)\vec{v}$$
Nota: se aplican de derecha a izquierda — $M_1$ primero, $M_2$ después.

**Longitud (norma) de un vector:**
$$|\vec{v}| = \sqrt{v_1^2 + v_2^2} \quad \text{(en 2D)}$$

---

## Ch 4 — Matrix Multiplication as Composition (2026-06-27)

**Core insight:** Matrix multiplication = composing two transformations into one.

- $M_2 M_1$ means: apply $M_1$ **first**, then $M_2$ (read right to left, like $f(g(x))$)
- The resulting matrix IS the single transformation that does both in sequence
- Order matters: "rotate then shear" ≠ "shear then rotate" → $AB \neq BA$ in general

**Mechanical recipe (derived from geometry):**

Each column of the result = $M_2$ applied to each column of $M_1$:

$$\begin{bmatrix}a&b\\c&d\end{bmatrix}\begin{bmatrix}e&f\\g&h\end{bmatrix} = \begin{bmatrix}ae+bg & af+bh\\ce+dg & cf+dh\end{bmatrix}$$

Why: columns of $M_1$ tell you where $\hat{i}$ and $\hat{j}$ land → $M_2$ transforms those landing spots → result encodes the full composition.

**Properties:**
- Associative: $(AB)C = A(BC)$ ✓
- NOT commutative: $AB \neq BA$ in general ✗

**Gap propio (quiz 2026-07-03):** contesté "el orden de los factores no altera el producto" — dije lo OPUESTO de lo correcto. Confundí con la propiedad conmutativa de números reales. En matrices el orden SÍ importa porque cada matriz es una transformación geométrica — $AB$ aplica $B$ primero, y la segunda transformación actúa sobre el espacio ya deformado por la primera. Repasar con un ejemplo concreto (rotar 90° luego cortar en x, vs cortar en x luego rotar 90°) para fijar la intuición geométrica, no solo la regla.

---

## Ch 5 — 3D Linear Transformations (2026-06-27)

**Core insight:** Everything from ch 4 generalizes to 3D — same logic, one extra basis vector.

- Now tracking where $\hat{i}$, $\hat{j}$, **and** $\hat{k}$ land → 3×3 matrix (3 columns, one per basis vector)
- Composition still works the same: $A \cdot B$ = apply B first, then A
- Used in **computer graphics** (rotating 3D objects) and **robotics** (joint transformations)

**Why it matters for ML:** Neural network weight matrices are N×M — same principle, just N-dimensional space. A layer `y = Wx` is literally a linear transformation from M-dim to N-dim space.

---

## Ch 6 — The Determinant (2026-06-27)

**Core insight:** The determinant is the **scale factor** by which a transformation stretches or shrinks area (2D) or volume (3D).

- Matrix $\begin{bmatrix}3&0\\0&2\end{bmatrix}$ → det = 6 → every region in space gets scaled by 6×
- The determinant applies uniformly to **any** shape, not just the unit square

**Formula (2D):**
$$\det\begin{bmatrix}a&b\\c&d\end{bmatrix} = ad - bc$$

Geometric derivation: the parallelogram area = $(a+b)(c+d) - ac - bd - 2bc = ad - bc$

- When $b=0, c=0$: det $= ad$ (pure scale — just width × height)
- When $b \neq 0, c=0$: det still $= ad$ — **shear doesn't change area** (the parallelogram tilts but its base × height stays constant)
- When $c \neq 0$: the $bc$ term accounts for how much the parallelogram is stretched/compressed

**Special values:**
- **det = 0** → space collapsed to a lower dimension (line, plane, or point) — transformation is not invertible, information lost permanently
- **det < 0** → orientation flipped. In 2D: $\hat{i}$ and $\hat{j}$ swap from counterclockwise to clockwise. In 3D: right-hand rule violated ("principle of hand")

**In 3D:** determinant = scale factor for **volume**. Unit cube deforms into a parallelepiped; det = how much that volume changed.

**Key property:**
$$\det(AB) = \det(A) \times \det(B)$$
If you apply two transformations, the total area scaling = product of each individual scaling.

**Why it matters for ML:**
- det = 0 → matrix is singular → not invertible → that layer loses information (squashes multiple inputs to the same output)
- Understanding when transformations preserve vs. destroy information is core to understanding gradient flow and network expressiveness

---

## Ch 7 — Inverse Matrices, Column Space, Null Space (2026-06-27)

**Core use of linear algebra:** Solving systems of linear equations. Each variable is scaled by a constant and summed — that's exactly $A\vec{x} = \vec{v}$.

**Rewriting a system as a matrix equation:**
$$2x+5y+3z=-3 \quad \rightarrow \quad \begin{bmatrix}2&5&3\\4&0&8\\1&3&0\end{bmatrix}\begin{bmatrix}x\\y\\z\end{bmatrix}=\begin{bmatrix}-3\\0\\2\end{bmatrix}$$

Goal: find $\vec{x}$ such that $A$ transforms it into $\vec{v}$.

**Solving with the inverse:**
- If det(A) ≠ 0: unique solution exists → $\vec{x} = A^{-1}\vec{v}$
- $A^{-1}A = I$ (identity — "the transformation that does nothing")
- Geometrically: $A^{-1}$ runs the transformation backwards

**How to compute $A^{-1}$ (2×2):**

$$A = \begin{bmatrix}a&b\\c&d\end{bmatrix} \quad \rightarrow \quad A^{-1} = \frac{1}{\det(A)}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$$

Steps: (1) swap diagonal $a \leftrightarrow d$, (2) negate off-diagonal, (3) divide by det.

For 3×3+: use `numpy.linalg.inv(A)` — concept is identical, formula is messy.

**Concrete example:**
$$2x + y = 5, \quad x + 3y = 7$$
$$A = \begin{bmatrix}2&1\\1&3\end{bmatrix}, \quad \det(A) = (2)(3)-(1)(1) = 5 \neq 0$$
$$A^{-1} = \frac{1}{5}\begin{bmatrix}3&-1\\-1&2\end{bmatrix}$$
$$\vec{x} = A^{-1}\vec{v} = \frac{1}{5}\begin{bmatrix}3&-1\\-1&2\end{bmatrix}\begin{bmatrix}5\\7\end{bmatrix} = \frac{1}{5}\begin{bmatrix}8\\9\end{bmatrix} = \begin{bmatrix}1.6\\1.8\end{bmatrix} \checkmark$$
Verify: $A^{-1}A = I$ ✓ — "the transformation that does nothing"

**When det(A) = 0 — no inverse exists:**
Space got compressed to a lower dimension — you can't "undo" that. Solutions only exist if $\vec{v}$ happens to live in that compressed output space.

**Rank** = number of dimensions in the output (column space):
- Rank 3 (full rank, 3×3): output fills all of 3D space
- Rank 2: output is a plane
- Rank 1: output is a line

**Column space** = set of all possible outputs of $A\vec{x}$ — the "span" of A's columns.

**Null space / Kernel** = all input vectors that get squashed to $\vec{0}$.

Concrete example — $A = \begin{bmatrix}1&2\\2&4\end{bmatrix}$, det = 0:
- Column space: line spanned by $\begin{bmatrix}1\\2\end{bmatrix}$ (rank 1)
- Null space: line spanned by $\begin{bmatrix}2\\-1\end{bmatrix}$ — these inputs are destroyed

**Intuition:** rank = what survives. null space = what gets destroyed.

**Why it matters for ML:**
- Weight matrix with rank < N → information bottleneck (not all dimensions used)
- Null space of a weight layer = directions in input space the network is completely blind to
- Solving $A\vec{x} = \vec{v}$ is at the heart of least-squares regression and linear probes

**Gap propio (quiz 2026-07-07, biweekly-cumulative):** null space → dije "se aplasta a un punto", falta el detalle clave: se aplasta al **vector cero** específicamente (no cualquier punto), y no siempre es un punto — puede ser línea/plano según el rank. Y en det(A)=0 → di la geometría bien pero omití la consecuencia práctica: no hay solución única para $A\vec{x}=\vec{v}$.

---

## Ch 8 — Nonsquare Matrices (2026-06-27)

**Core insight:** A nonsquare matrix transforms between spaces of different dimensions.

- **3×2 matrix**: takes 2D input → 3D output (embeds a plane into 3D space). Column space = a plane inside 3D.
- **2×3 matrix**: takes 3D input → 2D output (projects down, loses one dimension)
- Columns = number of input dimensions (basis vectors going in)
- Rows = number of coordinates in the output (where those basis vectors land)

**The matrix multiplication dimension rule:**
$$(m \times n) \cdot (n \times p) = (m \times p)$$
Inner dimensions must match. Outer dimensions give result shape.

| A | B | Valid? | Result |
|---|---|--------|--------|
| 3×2 | 2×4 | ✓ | 3×4 |
| 2×3 | 3×5 | ✓ | 2×5 |
| 2×3 | 2×3 | ✗ | — |

**Why this matters for ML (critical):**
Every neural network layer is a nonsquare matrix multiply: `y = Wx + b`
- W shape = (output_dim × input_dim)
- 784 pixels → (256×784) W → 256-dim hidden layer → (10×256) W → 10 class scores
- Full rank = preserves as much info as possible given the compression

---

## Ch 9 — Dot Products and Duality (2026-06-29)

**El resultado:** un número (escalar). Mide cuánto apuntan dos vectores en la misma dirección.

**Fórmula algebraica:**
$$\vec{v} \cdot \vec{w} = v_1 w_1 + v_2 w_2 + \ldots + v_n w_n$$

**Fórmula geométrica:**
$$\vec{v} \cdot \vec{w} = |\vec{v}||\vec{w}|\cos\theta$$

donde θ es el ángulo entre los dos vectores.

**Interpretación del signo:**
- `v·w > 0` → ángulo < 90° — apuntan "al mismo lado"
- `v·w = 0` → perpendiculares (ortogonales) — cero dirección compartida
- `v·w < 0` → ángulo > 90° — apuntan en direcciones opuestas

**Proyección — ¿cuánto de w va en dirección de v?**

Componente escalar (longitud de la "sombra" de w sobre v):
$$\text{comp}_{\vec{v}}\vec{w} = \frac{\vec{v} \cdot \vec{w}}{|\vec{v}|}$$

Proyección vectorial (el vector sombra completo):
$$\text{proj}_{\vec{v}}\vec{w} = \frac{\vec{v} \cdot \vec{w}}{|\vec{v}|^2}\vec{v}$$

**Para qué sirve la proyección:** responde "¿cuánto de w va en la dirección de v?" Ejemplo físico: fuerza F empujando en diagonal sobre un riel horizontal — `F · horizontal` da la fuerza efectiva.

**Dualidad (el insight profundo):**

Cualquier transformación lineal nD→1D puede escribirse de dos formas equivalentes:
1. Como una matriz fila `[u₁, u₂, ..., uₙ]` multiplicando un vector
2. Como producto punto con el vector û = `[u₁, u₂, ..., uₙ]`

Prueba con û = [0.6, 0.8]:
- î = [1,0] → [0.6, 0.8]·[1,0] = **0.6** (= coordenada x de û)
- ĵ = [0,1] → [0.6, 0.8]·[0,1] = **0.8** (= coordenada y de û)

Las coordenadas de û son exactamente donde aterrizan î y ĵ. Esto es la dualidad: proyectar = transformación lineal. Siempre hay un vector dual que hace lo mismo que la transformación.

**Generalización:** funciona para cualquier dimensión. Si la transformación aplana nD→1D, existe un vector en nD que es su dual. Para 3D→1D: vector dual vive en 3D. Para 100D→1D: vector dual vive en 100D.

**Gap propio (quiz 2026-07-03):** pedido "explicá dualidad en una oración" → no recordé nada. Segunda vez que este concepto no sobrevive el gap entre sesiones (ya había fallado el cross-product-vía-dualidad en el quiz de 2026-06-30). Necesita repaso desde cero, no solo repregunta — probablemente ayude reforzar con el ejemplo concreto de arriba (û=[0.6,0.8]) antes de pedir la definición abstracta.

**Gap propio (quiz 2026-07-07, biweekly-cumulative):** TERCERA vez que dualidad falla — esta vez parcial ("podemos resolver a espacio 1D usando ambos transformaciones o producto punto"), rondando la idea pero sin decir la equivalencia exacta. El concepto no está afianzado — necesita re-explicación estructurada (no solo repetir la definición), quizás con un diagrama o comparación lado-a-lado matriz-fila vs producto-punto antes de la próxima ronda.

**Repaso 2026-07-22 (rewatch completo, no solo repregunta):** lo que hizo clic fue la secuencia "¿dónde aterrizan î y ĵ al proyectarlos sobre la recta de û?" → esas 2 proyecciones SON las 2 entradas de la matriz 1×2 → `[ux uy][x,y] = ux·x+uy·y = [ux,uy]·[x,y]`, matriz-fila y dot-product son la misma cuenta. Confirmación propia: "es una transformation entonces igual el producto punto? sí." Requiere û **unitario** específicamente — ver [[vector-unitario-normalizacion]] (repasado en la misma sesión, gap aparte). Detalle completo: [[dot-product-duality-explained]].

**Por qué importa en ML/AI:**
- **Cosine similarity** = producto punto de vectores unitarios = cos(θ) entre embeddings
- **Attention** en transformers = una matriz de productos punto (Q·Kᵀ) — mide qué tan "similares" son queries y keys
- Cada neurona en una red hace un producto punto: `w·x` — ¿cuánto del input va en la dirección del peso?

**Ejemplo numérico completo:**

v = [3, 1], w = [2, 4]:
- Algebraico: `3×2 + 1×4 = 10`
- Geométrico: `|v| = √10, |w| = √20, cos(θ) = 10/(√10·√20) = 10/√200 ≈ 0.707` → θ ≈ 45°
- Proyección de w sobre v: `10/√10 ≈ 3.16` (longitud de la sombra)

---

## Ch 10 — Cross Products (2026-06-29)

**El resultado:** un vector (en 3D). Perpendicular a los dos vectores de entrada.

Solo definido en 3D (y matemáticamente en 7D, ignorar eso).

**Fórmula:**
$$\vec{v} \times \vec{w} = \det\begin{bmatrix}\hat{i} & \hat{j} & \hat{k} \\ v_x & v_y & v_z \\ w_x & w_y & w_z\end{bmatrix} = \begin{bmatrix}v_y w_z - v_z w_y \\ v_z w_x - v_x w_z \\ v_x w_y - v_y w_x\end{bmatrix}$$

**Fórmula geométrica para la magnitud:**
$$|\vec{v} \times \vec{w}| = |\vec{v}||\vec{w}|\sin\theta$$

= área del paralelogramo formado por v y w.

**Regla de la mano derecha:** dedos de v a w → el pulgar apunta en la dirección de v×w.

**Nota sobre la fórmula del determinante:** el determinante con î, ĵ, k̂ como fila NO es un determinante real (determinantes toman escalares, no vectores) — es un truco mnemotécnico. Al expandirlo, los vectores base actúan como placeholders para las componentes del resultado, no como entradas reales de matriz. Un determinante 3×3 real siempre tiene solo escalares.

**Determinante 3×3 real (comparación, solo escalares):**
$$\det\begin{bmatrix}a&b&c\\d&e&f\\g&h&i\end{bmatrix} = a(ei-fh) - b(di-fg) + c(dh-eg)$$

**Expansión del "determinante" mnemotécnico → fórmula de v×w:**
$$\vec{v}\times\vec{w} = \hat{i}(v_yw_z-v_zw_y) - \hat{j}(v_xw_z-v_zw_x) + \hat{k}(v_xw_y-v_yw_x)$$
$$= \begin{bmatrix}v_yw_z-v_zw_y\\v_zw_x-v_xw_z\\v_xw_y-v_yw_x\end{bmatrix}$$

Misma estructura de cofactores que el determinante real — por eso el truco funciona — pero aquí cada cofactor multiplica un vector base en vez de sumarse a un escalar único.

**Ojo — no confundir con "determinante = escala de área" (ch6):** son 2 cosas distintas con el mismo nombre.
- Determinante real (ch6): número, factor de escala de área/volumen de una transformación.
- Mnemotécnico aquí: no escala nada — calcula las 3 componentes del vector v×w.
- La relación con área es aparte: $|\vec{v}\times\vec{w}|$ (la norma del vector resultado) = área del paralelogramo. Ver [[determinante-vs-cross-product-mnemonic]].

**Signo importa:**
- `v×w` = -(w×v) — anticonmutativo

**Por qué importa en ML/AI:**
- Menos directo que el producto punto, pero clave en geometría 3D
- Se usa para calcular normales de superficies (gráficos 3D, visión computacional)
- Aparece en física (torque, momento angular) que subyace a simulaciones físicas en RL

**Repaso 2026-07-22 (rewatch completo):**

*Caso 2D primero (antes de saltar a 3D):* `v×w = det([v w])` — mismo determinante 2×2 de ch6, pero acá el resultado ES el área con signo del paralelogramo, no un factor de escala de otra transformación.

*Regla de orientación (signo):* girás de v hacia w por el camino más corto — antihorario → positivo, horario → negativo. Propio: necesité 2 correcciones acá — primer intento mezclaba la regla con î/ĵ específicamente en vez de v,w genéricos; luego el fraseo "w antes q v" seguía ambiguo. La forma que finalmente quedó clara: "giro de v a w, ¿horario o antihorario?" — no pensar en posiciones relativas, pensar en la dirección del giro.

*Por qué perpendiculares dan cross product más grande:* al acercarse a paralelos, el paralelogramo se "aplasta" — la altura efectiva tiende a 0 aunque los lados midan igual. Perpendiculares = altura máxima = área máxima, para largos de vector fijos.

*Escalado:* `(3v)×w = 3(v×w)` — escalar un vector de entrada escala el área linealmente, igual que en dot product (homogeneidad).

*En 3D — vector, no escalar:* dirección perpendicular al paralelogramo (regla mano derecha), longitud = área del paralelogramo (la misma cantidad que en el caso 2D con signo, ahora como magnitud del vector resultado).

---

## Ch 11 — Cross Product como Dualidad (2026-06-29)

**El insight:** el producto cruz es la dualidad aplicada a 3D.

Define una función: f(v) = det([v, w₁, w₂]) — toma v en 3D y produce un número (el volumen del paralelepípedo). Esa función es lineal en v.

Por dualidad: existe un vector p tal que f(v) = p·v para todo v.

Ese vector p = w₁ × w₂.

**Conclusión:** el producto cruz es "el vector dual de la función volumen definida por dos vectores". La fórmula del producto cruz no es magia — es la consecuencia directa de aplicar dualidad al determinante 3D.

**Repaso 2026-07-22 (gap cerrado — era el pendiente desde 06-30, falló en quiz de esa fecha):**

Derivación completa, paso a paso:
1. f([x,y,z]) = det([x,v1,w1 / y,v2,w2 / z,v3,w3]) — función de volumen, v,w fijos.
2. Lineal → por dualidad existe p único tal que f([x,y,z]) = p·[x,y,z] para todo [x,y,z].
3. Se resuelve p igualando coeficientes (x, y, z) entre p1x+p2y+p3z y la expansión del determinante → p1=v2w3-v3w2, p2=v3w1-v1w3, p3=v1w2-v2w1. Método: matching de coeficientes, no adivinar la fórmula.
4. p = v×w. Geométricamente: longitud = área del paralelogramo(v,w), dirección **perpendicular al plano de v,w** (no al paralelepípedo, que es un sólido 3D sin una única perpendicular).

**Confusión propia corregida:** área×perpendicular NO es cómo se construye p — es la lectura geométrica del resultado ya derivado por dualidad. Ver [[cross-product-derivacion-vs-interpretacion]] y el visual paso a paso [cross-product-duality-derivation-2026-07-22.html](../07-Visuals/cross-product-duality-derivation-2026-07-22.html).

Quiz cerrado en la misma sesión: 3/3 sin nudges — mejor resultado que ch9 (que necesitó 3 fallos previos + hoy). Este concepto quedó afianzado en un solo repaso.

---

> **Nota:** el contenido formal de Axler (subespacios, independencia lineal, bases, dimensión, mapas lineales) se movió a [[Linear-Algebra-Axler-Fundamentals]] — explicado con menos símbolos, más prosa, cita al libro. Esta nota se queda con la intuición geométrica de 3b1b.

## Ch 12 — Cramer's Rule (2026-07-28)

**El insight:** resolver A·x = b usando áreas de paralelogramos en vez de álgebra directa.

Sistema A = [[a,b],[c,d]], x=[x,y] desconocido, b conocido. Como b = x·col1 + y·col2:

- **Shear, no rotación:** el paralelogramo (col1, b) se desliza (shear) hasta (col1, y·col2) sin cambiar área — principio de Cavalieri. La parte x·col1 no aporta área extra porque está en la misma dirección que col1.
- área(col1, b) = y · det(A) → **y = área(col1, b) / det(A)**
- Análogo para x con área(b, col2) / det(A)

**No es la herramienta práctica:** el propio video lo dice — Gaussian elimination es más rápido, sobre todo en matrices grandes. `torch.linalg.solve` usa LU decomposition (Gauss), no Cramer. El valor de ch12 es reforzar la intuición área↔determinante (ch9-11) antes de eigenvalues (ch14).

Detalle completo, incluyendo la confusión shear-vs-rotación resuelta: [[cramers-rule-shear-not-rotation]].

---

## Ch 13 — Change of Basis (2026-07-28)

**El insight:** un vector no cambia — pero las coordenadas que le asignás dependen de qué vectores base uses. [3,2] siempre asume implícitamente la base estándar (î,ĵ); con otra base, el mismo punto en el espacio tiene otros números.

**Base de Jennifer:** b1=[2,1], b2=[-1,1] — descritos en NUESTRO lenguaje (nuestras coordenadas). Para Jennifer, sus propios vectores son simplemente [1,0] y [0,1] — su î,ĵ.

**Origen coincide:** ambos sistemas comparten el mismo origen, solo cambia la orientación/escala de la grilla.

### Traducir un vector

Matriz de cambio de base A = columnas [b1, b2] (en nuestro lenguaje):

$$A = \begin{bmatrix}2&-1\\1&1\end{bmatrix}$$

- A · (coordenadas de Jennifer) = coordenadas nuestras. Ejemplo: A·[-1,2] = -1·b1 + 2·b2 = [-4,1].
- A⁻¹ · (coordenadas nuestras) = coordenadas de Jennifer.

**Grid vs. Language — la parte contraintuitiva (verificado, 3B1B):**
> "Geometrically this matrix transforms our grid into Jennifer's grid, yet numerically it's translating a vector described in her language to our language."

A mueve la GRILLA de nosotros→Jennifer, pero traduce el LENGUAJE de Jennifer→nosotros. Direcciones opuestas — no es un error, es cómo funciona la dualidad grid/coordenadas.

### Traducir una transformación — el sandwich A⁻¹MA

M = una transformación que solo "habla" nuestro lenguaje (ej. rotar 90°). Para aplicarla a un vector v_J dado en coordenadas de Jennifer:

1. A·v_J → traduce a nuestro lenguaje
2. M·(A·v_J) → aplica la transformación (que entiende nuestro lenguaje)
3. A⁻¹·(M·A·v_J) → traduce el resultado de vuelta al lenguaje de Jennifer

**A⁻¹MA = la misma transformación M, descrita en el idioma de Jennifer.**

Cita textual (verificada, 3B1B):
> "In general, whenever you see an expression like A⁻¹MA, it suggests a mathematical sort of empathy. The middle matrix represents a transformation as you see it, the outer two matrices represent the empathy, this shift in perspective, and the full matrix product represents that same transformation as someone else sees it."

**Por qué importa para ML:** cambio de base es la base matemática de PCA (encontrar la base donde los datos se ven más simples) y de por qué normalizar/estandarizar features es, literalmente, un cambio de coordenadas.

**Gap propio (sesión 2026-07-28):** el sandwich A⁻¹MA confundió inicialmente — la corrección clave fue distinguir "grid" (A traduce ours→Jennifer) de "language" (A traduce Jennifer→ours), direcciones opuestas del mismo A. Ver [[change-of-basis-a-inverse-m-a]].

---

## Ch 14 — Eigenvectors and Eigenvalues (2026-08-05)

**El insight central:** al aplicar una transformación A, la mayoría de los vectores se salen de su span original (rotan/se desvían). Un **autovector** es de los pocos que se quedan sobre su propia línea (span) — solo se estira o encoge, nunca rota. El factor de estiramiento es su **autovalor** asociado.

$$A\vec{v} = \lambda\vec{v}$$

Ejemplo trabajado con A=[[3,1],[0,2]]:
- î=[1,0] queda sobre el eje x (su propio span) tras la transformación → autovector con λ=3 (columna 1 de A es [3,0], 3 veces î). [-1,1] se estira a 2·[-1,1] → autovector con λ=2.
- Un vector cualquiera (ej. amarillo intermedio) se sale de su span — no es autovector.

**Por qué es útil:** en 3D, un autovector de una rotación es literalmente el **eje de rotación** — el único vector que no se mueve. Patrón general en álgebra lineal: cuando algo parece depender de la orientación de tus ejes (coordenadas), buscá si en realidad depende solo de los autovectores/autovalores — esos son intrínsecos a la transformación, no a cómo elegiste describirla.

### Derivando el cálculo — det(A − λI) = 0

Problema: `Av = λv` tiene tipos distintos a cada lado (matriz·vector vs escalar·vector). Truco: `λv = λ(Iv) = (λI)v` — ahora ambos lados son matriz·vector, se puede restar:

$$A\vec{v} = \lambda\vec{v} \;\Rightarrow\; (A-\lambda I)\vec{v} = \vec{0}$$

Esto pide un vector v≠0 en el null space de `(A-λI)` — por ch7, eso solo pasa cuando la transformación colapsa una dimensión, es decir `det(A-λI) = 0` (ver [[eigen-lambda-i-trick]] para el paso a paso completo de por qué se multiplica por I).

**Ejemplo — A=[[3,1],[0,2]]:**
$$\det\begin{bmatrix}3-\lambda & 1\\0 & 2-\lambda\end{bmatrix} = (3-\lambda)(2-\lambda) = 0 \;\Rightarrow\; \lambda=2 \text{ o } \lambda=3$$

Con λ=2: resolver `[[1,1],[0,0]]v=0` → autovector en la dirección [-1,1] (o cualquier múltiplo).
Con λ=3: autovector [1,0] (î).

**Caso sin autovectores reales — rotación pura:**
$$\det\begin{bmatrix}-\lambda & -1\\1 & -\lambda\end{bmatrix} = \lambda^2+1=0 \;\Rightarrow\; \lambda=\pm i$$

Autovalores complejos → ninguna dirección real se queda fija. Consistente con la intuición geométrica: una rotación (sin escala) mueve *todo* vector fuera de su span, salvo el caso trivial 180°.

### Truco mental para 2×2 — mean ± √(mean²-product)

Para una matriz 2×2, dos atajos evitan expandir el polinomio característico completo:

- **Traza = suma de autovalores**: $\text{tr}(A) = a+d = \lambda_1+\lambda_2$
- **Determinante = producto de autovalores**: $\det(A) = ad-bc = \lambda_1\lambda_2$

Conocer suma y producto de 2 números es el mismo problema que factorizar `x²-Sx+P=0`. Con `m = tr(A)/2` (promedio) y `p = det(A)` (producto):

$$\lambda_1,\lambda_2 = m \pm \sqrt{m^2-p}$$

Es la fórmula cuadrática de siempre, reescrita: viene de `λ²-2mλ+p=0` → `λ=(2m±√(4m²-4p))/2 = m±√(m²-p)`. Ventaja: `m` y `p` se leen directo de la matriz (traza/2 y determinante) sin expandir el polinomio característico símbolo por símbolo — menos pasos que identificar a,b,c en `(-b±√(b²-4ac))/2a`.

**Ejemplo — A=[[8,4],[2,6]]:** m=(8+6)/2=7, p=8·6-4·2=40 → d²=7²-40=9 → d=3 → λ=4 o λ=10.

**Ejemplo — A=[[3,11],[1,11]]:** m=(3+11)/2=7, p=3·11-11·1=22 → λ=7±√(49-22)=7±√27.

Confirmado contra la fuente oficial — [3Blue1Brown, "A quick trick for computing eigenvalues"](https://www.3blue1brown.com/lessons/quick-eigen/).

### Diagonalización — base de autovectores

Si los propios vectores base de un sistema de coordenadas son autovectores, la matriz en esa base es **diagonal** (0 en todas partes salvo la diagonal). Diagonal = trivial de exponenciar: $D^n$ eleva cada entrada a la n independientemente — no hay que multiplicar matrices repetidamente.

**Cambio a base de autovectores** (mismo sandwich A⁻¹MA de Ch13 arriba, con M=matriz de autovectores como columnas):

$$M^{-1}AM = D \quad\Rightarrow\quad A^n = M D^n M^{-1}$$

Con A=[[3,1],[0,2]], autovector [-1,1] como nueva base:
$$\begin{bmatrix}1&-1\\0&1\end{bmatrix}^{-1}\begin{bmatrix}3&1\\0&2\end{bmatrix}\begin{bmatrix}1&-1\\0&1\end{bmatrix} = \begin{bmatrix}3&0\\0&2\end{bmatrix}$$

**Por qué es raro tener suerte:** no toda matriz tiene una base completa de autovectores reales (ver caso rotación arriba) — cuando SÍ los tiene, calcular potencias grandes ($A^n$ para n gigante) se vuelve trivial en vez de multiplicar A por sí misma n veces.

### Aplicación práctica — Fibonacci vía eigenbasis

Ejercicio resuelto en código: A=[[0,1],[1,1]] tiene la propiedad `Aⁿ = [[F(n-1),F(n)],[F(n),F(n+1)]]`. Sus autovalores son las raíces de `λ²-λ-1=0`: φ=(1+√5)/2 (razón áurea) y ψ=(1-√5)/2 — literalmente los ingredientes de la fórmula de Binet, `F(n) = (φⁿ-ψⁿ)/√5`. Diagonalizar y exponenciar en la base de autovectores da Fⁿ en O(1) multiplicaciones de escalares en vez de O(n) multiplicaciones de matrices.

Código + tests: [`05-Projects/eigenvectors-3b1b/src/eigenvectors_3b1b/fib_eigen.py`](../05-Projects/eigenvectors-3b1b/src/eigenvectors_3b1b/fib_eigen.py) — `matrix_power_via_eigenbasis` implementa la fórmula genérica, `fib(n)` la aplica a Fibonacci, tests verifican contra cálculo directo y contra `np.linalg.matrix_power`.

Visualizador interactivo (sliders para a,b,c,d de la matriz, dibuja grid transformado + spans de autovectores en vivo): [`05-Projects/eigenvectors-3b1b/src/eigenvectors_3b1b/visualize.py`](../05-Projects/eigenvectors-3b1b/src/eigenvectors_3b1b/visualize.py) — correr con `uv run python -m eigenvectors_3b1b.visualize` desde esa carpeta.

**Por qué importa para ML/AI:**
- **PCA:** los componentes principales son los autovectores de la matriz de covarianza de los datos; el autovalor asociado = varianza capturada en esa dirección. El primer componente principal es el autovector con mayor autovalor. (Livins, *Eigenvalues and Principal Component Analysis*, Medium; apxml.com, *Eigenvectors Role in PCA*)
- Aparece de nuevo más adelante en self-attention y en análisis de estabilidad de redes recurrentes (autovalores >1 → explosión, <1 → desvanecimiento — mismo patrón que vanishing/exploding gradients).

**Gap propio (quiz cumulative 2026-08-05):** conexión dot-product→attention (Q·Kᵀ) fallada — normal, es preview de Phase 2 todavía no cubierto formal.

---

## Still to cover (3B1B chapters 15)
- Ch 15: Abstract vector spaces

---

## Why it matters for AI

Cada capa de una red neuronal es `y = Wx + b` — una multiplicación de matrices. Los embeddings son vectores en espacio de alta dimensión. Entender esto geométricamente separa "corro el código" de "entiendo qué está pasando".

## Resources

- [3Blue1Brown — Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)
- [Mathematics for Machine Learning, Ch. 2](https://mml-book.github.io/)
- [Eigenvalues and Principal Component Analysis — Medium](https://medium.com/@sirtonylivins/eigenvalues-and-principal-component-analysis-7f2f44c68ed6)
- [The Fibonacci sequence and linear algebra — Fabian Dablander](https://fabiandablander.com/r/Fibonacci.html)

## Doubts Resolved

- [[cross-product-real-world-ml-uses]] — para qué sirve cross product en mundo real y ML (2026-06-30)
- [[duality-in-neural-networks]] — cómo duality explica por qué cada neurona es un dot product (2026-06-30)
- [[determinante-vs-cross-product-mnemonic]] — determinante real (escala área) vs. mnemotécnico del cross product (vector) — no son lo mismo (2026-06-30)
- [[dot-product-duality-explained]] — producto punto: geometria vs componentes, por qué coinciden (2026-06-30); repaso 4to intento 2026-07-22, finalmente afianzado
- [[vector-unitario-normalizacion]] — qué es vector unitario y por qué û unitario es clave en la equivalencia matriz-fila⇔dot-product (2026-07-22)
- [[cross-product-derivacion-vs-interpretacion]] — v×w se deriva por dualidad, área×perpendicular es lectura geométrica del resultado, no ingrediente del cálculo (2026-07-22)
- [[cramers-rule-shear-not-rotation]] — la "matriz que gira" en Cramer's rule es en realidad un shear (Cavalieri), no rotación; quién la creó; por qué Gauss gana en la práctica (2026-07-28)
- [[change-of-basis-a-inverse-m-a]] — el sandwich A⁻¹MA: por qué "grid" y "language" de la matriz de cambio de base van en direcciones opuestas, y qué significa "traducir una transformación" (2026-07-28)
- [[eigen-lambda-i-trick]] — por qué λv se reescribe como (λI)v antes de poder factorizar (A-λI)v=0 (2026-08-05)
