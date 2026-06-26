---
tags: [phase-0, math, linear-algebra]
status: learning
first_learned: 2026-06-26
last_reviewed: 2026-06-26
confidence: 2/5
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

## Still to cover (3B1B chapters 4–16)

- Determinantes
- Producto punto y dualidad
- Producto cruz
- Matrices inversas, espacio columna, espacio nulo
- Vectores y valores propios (eigenvectors/eigenvalues)

---

## Why it matters for AI

Cada capa de una red neuronal es `y = Wx + b` — una multiplicación de matrices. Los embeddings son vectores en espacio de alta dimensión. Entender esto geométricamente separa "corro el código" de "entiendo qué está pasando".

## Resources

- [3Blue1Brown — Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)
- [Mathematics for Machine Learning, Ch. 2](https://mml-book.github.io/)

## Doubts Resolved

<!-- Link any resolved doubts from /06-Doubts-Resolved/ here -->
