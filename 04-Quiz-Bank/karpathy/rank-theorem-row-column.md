---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - coding-the-matrix
  - klein
  - dimension
  - rank
self-explain: true
noteId: 1785990658639
---
¿Qué dice el Rank Theorem, y a grandes rasgos cómo se prueba (idea de A=BU)?

---

Row rank = column rank, para cualquier matriz. Se prueba escribiendo A=BU (B=base del column space, U=coordenadas de cada columna en esa base). Reinterpretando la misma ecuación por filas, cada fila de A resulta combinación lineal de las filas de U → row rank(A) ≤ column rank(A). Aplicando el mismo argumento a la transpuesta Aᵀ da la desigualdad al revés (column rank(A) ≤ row rank(A)). Las dos juntas fuerzan la igualdad.

Ref: `02-Topics/Coding-the-Matrix-Basis.md — 9. Dimensión y Rank`
