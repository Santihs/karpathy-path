---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785651973694
---
¿Por qué `(αu)·(αv) ≠ α(u·v)` en general (Problem 2.9.24)?

---

El escalar se aplica a AMBOS lados del dot-product, así que se duplica: `(αu)·(αv) = α²(u·v)`, no `α(u·v)`. Homogeneity solo garantiza escalar UN lado a la vez.

Ref: `02-Topics/Coding-the-Matrix-Vectors.md — 10.5 Propiedades algebraicas del dot-product`
