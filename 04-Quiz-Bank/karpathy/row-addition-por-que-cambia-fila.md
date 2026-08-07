---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - gaussian-elimination
noteId: 1786145495437
---
En Gaussian elimination, ¿por qué cambian TODOS los valores de una fila (no solo la columna del pivot) al hacer una row-addition operation?

---

Porque se resta el vector ENTERO de la fila pivot escalado, no solo la entrada de esa columna: `row_nuevo = row - multiplier*pivot_row`.

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.1 — Echelon form`
