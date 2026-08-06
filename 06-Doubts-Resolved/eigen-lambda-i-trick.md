---
tags: [phase-0, linear-algebra, eigenvectors]
date_resolved: 2026-08-05
---

# ¿Por qué λv se reescribe como (λI)v?

**La duda:** en la ecuación de autovalores `A·v = λ·v`, el lado izquierdo es matriz·vector y el lado derecho es escalar·vector — tipos distintos. ¿Por qué el video multiplica por la identidad para convertirlo en `A·v = (λI)·v`?

**La respuesta:** para restar los dos lados y factorizar `v`, ambos lados tienen que ser el mismo tipo de operación (matriz·vector). La identidad `I` no cambia nada (`I·v = v` por definición), así que:

```
λv = λ(Iv) = (λI)v
```

Ahora ambos lados son matriz·vector:
```
Av = (λI)v
Av - (λI)v = 0
(A - λI)v = 0
```

Esta última forma es la que importa: `(A - λI)` es una matriz. La ecuación dice "existe un vector v (no cero) que esta matriz manda a 0" — eso es exactamente la definición de null space no-trivial, que solo pasa cuando `det(A - λI) = 0` (ver [[Linear-Algebra-Basics]] Ch 7, null space / rank).

## Fuentes

- [3Blue1Brown — Essence of Linear Algebra, Ch 14: Eigenvectors and eigenvalues](https://www.3blue1brown.com/topics/linear-algebra) — derivación completa en video, verificado contra los frames pegados en la sesión.
