---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785651973743
---
Si `rowlist[i][i] == 0` en un sistema triangular, ¿qué implica matemáticamente (Prop. 2.11.6), y qué se hace en la práctica cuando la matriz general (no triangular) tiene ese problema?

---

Implica que existe al menos un `b` para el cual el sistema NO tiene solución — no es solo un límite del código. En la práctica (matriz no triangular pero invertible) se usa *partial pivoting*: reordenar filas para mover un valor no-cero a la diagonal — es la `P` en `A=PLU` que usa LAPACK `getrf` (la rutina detrás de `torch.linalg.solve`). Si ningún reordenamiento alcanza, la matriz es singular de verdad — ahí ya no aplica triangular solve.

Ref: `05-Projects/coding-the-matrix/src/coding_the_matrix/triangular.py`
