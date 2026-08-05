---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785651973594
---
En `triangular_solve_n`, la línea `x[i] = (b[i] - rowlist[i] * x) / rowlist[i][i]` usa dot-product. ¿Cómo hace el dot-product para "ignorar" las variables todavía no resueltas?

---

`x` arranca en el vector cero y se llena de atrás para adelante. Las posiciones todavía no resueltas valen 0 en `x`, así que en el dot-product `coef * 0 = 0` — no aportan nada a la suma automáticamente, sin lógica especial.

Ref: `05-Projects/coding-the-matrix/src/coding_the_matrix/triangular.py`
