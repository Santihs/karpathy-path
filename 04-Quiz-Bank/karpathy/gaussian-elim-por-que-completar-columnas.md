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

Porque una fila puede tener valores no-cero que recién se cancelan en una columna posterior — cortar antes revela ese "falso positivo" y sobreestima el rank/independencia.

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.1 — Echelon form`
