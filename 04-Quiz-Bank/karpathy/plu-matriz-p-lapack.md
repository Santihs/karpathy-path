---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785903293253
---
En la factorización A=PLU, ¿qué representa la matriz P, y dónde aparece en la práctica (ML/dev)?

---

P es la matriz de permutación del partial pivoting; es la que usa LAPACK `getrf`, la rutina detrás de `torch.linalg.solve`.

Ref: `05-Projects/coding-the-matrix/src/coding_the_matrix/triangular.py`
