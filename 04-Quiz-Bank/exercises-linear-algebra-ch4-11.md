---
tags: [phase-0, linear-algebra, exercises, determinant, null-space, dot-product, cross-product, duality]
date_added: 2026-06-30
---

# Ejercicios a mano — Linear Algebra (ch4-11)

Generados tras quiz 2026-06-30 (score 3.5/5). Enfocados en gaps: det/null space (impreciso) y cross product vía dualidad (fallado).

No mires las respuestas hasta terminar cada bloque.

---

## Bloque 1 — Determinante y null space

**1.1** $A = \begin{bmatrix}2 & 4\\1 & 2\end{bmatrix}$

a) Calcula det(A).
b) ¿Tiene solución única $A\vec{x} = \begin{bmatrix}3\\1\end{bmatrix}$? Justifica.
c) Encuentra el null space de A (vector(es) base).

**1.2** $B = \begin{bmatrix}1 & 0 & 2\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}$

a) ¿Cuál es el rank de B?
b) Describe el column space (¿línea, plano, o todo el espacio 3D?).
c) Encuentra el null space de B.

---

## Bloque 2 — Dot product / proyección

**2.1** v = [4, 3], w = [1, 2]

a) Calcula v·w (algebraico).
b) Calcula |v| y usa la fórmula geométrica para hallar cos(θ).
c) Calcula comp_v(w) — cuánto de w va en dirección de v.

**2.2** v = [-1, 2], w = [3, 6]

a) Calcula v·w. ¿Qué signo tiene? ¿Qué te dice del ángulo entre ellos?
b) ¿v y w son perpendiculares? ¿Por qué sí o no?

---

## Bloque 3 — Cross product (cálculo directo)

**3.1** v = [1, 0, 0], w = [0, 1, 0]

a) Calcula v×w usando la fórmula de componentes.
b) Calcula w×v. Verifica: ¿w×v = -(v×w)?

**3.2** v = [2, 1, -1], w = [1, 3, 2]

a) Calcula v×w.
b) Calcula |v×w| (la magnitud).
c) ¿Qué representa ese número geométricamente?

---

## Bloque 4 — Dualidad (función lineal → vector dual)

**4.1** f(x, y, z) = 3x - 2y + 5z

a) f es lineal nD→1D. ¿Cuál es su vector dual û?
b) Verifica: calcula f(1, 1, 1) directamente, y luego calcula û · [1,1,1]. ¿Coinciden?

---

## Bloque 5 — Cross product vía dualidad (guiado, llena los blancos)

Usa v = [1, 2, 0], w = [0, 1, 3].

Paso 1: define f(x) = det([x, v, w]) donde x = [x, y, z]. Esta función es lineal en x.

Paso 2: por dualidad, existe un vector p tal que f(x) = p · x para todo x.

Paso 3: expande el determinante en componentes:
$$f(x,y,z) = \_\_\_\_ \cdot x + \_\_\_\_ \cdot y + \_\_\_\_ \cdot z$$

(Usa la fórmula: $p_1 = v_2w_3-v_3w_2$, $p_2 = v_3w_1-v_1w_3$, $p_3 = v_1w_2-v_2w_1$ — sustituye los valores de v y w de arriba.)

Paso 4: entonces p = [___, ___, ___] = v×w.

Paso 5: verifica calculando v×w directamente con la fórmula de componentes (como en bloque 3). ¿Coincide con tu p del paso 4?

---
---

# Respuestas

**1.1** a) det = (2)(2)-(4)(1) = 0. b) No hay solución única — det=0 significa espacio colapsado a una línea; solo hay solución si [3,1] cae en esa línea (columna de A: [2,1] escalado — [3,1] no es múltiplo de [2,1], así que NO hay solución). c) Null space: vectores [x,y] tales que 2x+4y=0 y x+2y=0 → misma ecuación → x=-2y → base: [-2,1] (o cualquier escalar).

**1.2** a) Rank = 2 (dos filas no-cero independientes). b) Column space = un plano en 3D (rank 2 de 3 posibles). c) Null space: Bx=0 → x+2z=0, y=0, z libre → base: [-2,0,1].

**2.1** a) v·w = 4(1)+3(2) = 10. b) |v|=5, |w|=√5, cos θ = 10/(5√5) ≈ 0.894 → θ≈26.6°. c) comp = 10/5 = 2.

**2.2** a) v·w = -3+12 = 9 > 0 → ángulo agudo (<90°), apuntan "al mismo lado". b) No son perpendiculares (v·w ≠ 0).

**3.1** a) v×w = [0·0-0·1, 0·0-1·0, 1·1-0·0] = [0,0,1] (= k̂, correcto: î×ĵ=k̂). b) w×v = [0,0,-1] = -(v×w) ✓.

**3.2** a) v×w = [(1)(2)-(-1)(3), (-1)(1)-(2)(2), (2)(3)-(1)(1)] = [2+3, -1-4, 6-1] = [5, -5, 5]. b) |v×w| = √(25+25+25) = √75 ≈ 8.66. c) Área del paralelogramo formado por v y w.

**4.1** a) û = [3, -2, 5] (coeficientes directos). b) f(1,1,1) = 3-2+5 = 6. û·[1,1,1] = 3-2+5 = 6. Coinciden ✓.

**5** v=[1,2,0], w=[0,1,3]. p1 = v2w3-v3w2 = 2(3)-0(1) = 6. p2 = v3w1-v1w3 = 0(0)-1(3) = -3. p3 = v1w2-v2w1 = 1(1)-2(0) = 1. p = [6,-3,1]. Verificación directa: v×w = [6,-3,1] ✓ coincide.
