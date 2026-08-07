---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - gaussian-elimination
noteId: 1786145495384
---
¿Qué problema numérico aparece en Gaussian elimination con floating-point cuando se restan múltiplos grandes de una fila?

---

"Swamping": un valor chico puede perderse frente a uno gigante (ej. `1 - 1e20 = -1e20` en Python, el 1 desaparece), dando rank mal calculado.

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.1.8-7.1.9 — Cuándo falla, y pivoting`
