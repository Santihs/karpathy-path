---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - gaussian-elimination
  - rank
noteId: 1786145495335
---
¿Por qué hay que procesar TODAS las columnas de Gaussian elimination antes de confiar en el rank/independencia calculado, en vez de parar cuando una fila "ya parece" tener contenido no-cero?

---

Porque hasta procesar todas las columnas no se puede saber si esa fila es redundante o si "le queda info escondida" en una columna aún no procesada — una fila puede tener valores no-cero que recién se cancelan al llegar a una columna posterior, revelando que era combinación lineal de las demás. Cortar antes de tiempo da un falso positivo de independencia (rank sobreestimado).

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.1 — Echelon form`
