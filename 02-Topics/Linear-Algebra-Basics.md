---
tags: [phase-0, math, linear-algebra]
status: learning
first_learned: 2026-06-26
last_reviewed: 2026-06-29
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

**Signo importa:**
- `v×w` = -(w×v) — anticonmutativo

**Por qué importa en ML/AI:**
- Menos directo que el producto punto, pero clave en geometría 3D
- Se usa para calcular normales de superficies (gráficos 3D, visión computacional)
- Aparece en física (torque, momento angular) que subyace a simulaciones físicas en RL

---

## Ch 11 — Cross Product como Dualidad (2026-06-29)

**El insight:** el producto cruz es la dualidad aplicada a 3D.

Define una función: f(v) = det([v, w₁, w₂]) — toma v en 3D y produce un número (el volumen del paralelepípedo). Esa función es lineal en v.

Por dualidad: existe un vector p tal que f(v) = p·v para todo v.

Ese vector p = w₁ × w₂.

**Conclusión:** el producto cruz es "el vector dual de la función volumen definida por dos vectores". La fórmula del producto cruz no es magia — es la consecuencia directa de aplicar dualidad al determinante 3D.

---

## Still to cover (3B1B chapters 12–16)

- Ch 12: Cramer's rule
- Ch 13: Change of basis
- Ch 14–15: Eigenvectors and eigenvalues (crítico para PCA, transformers)
- Ch 16: Abstract vector spaces

---

## Why it matters for AI

Cada capa de una red neuronal es `y = Wx + b` — una multiplicación de matrices. Los embeddings son vectores en espacio de alta dimensión. Entender esto geométricamente separa "corro el código" de "entiendo qué está pasando".

## Resources

- [3Blue1Brown — Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)
- [Mathematics for Machine Learning, Ch. 2](https://mml-book.github.io/)

## Doubts Resolved

<!-- Link any resolved doubts from /06-Doubts-Resolved/ here -->
