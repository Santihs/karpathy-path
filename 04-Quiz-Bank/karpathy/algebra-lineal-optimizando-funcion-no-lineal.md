---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - orthogonality
  - projection
  - machine-learning
  - gradient-descent
self-explain: true
noteId: 1786163375974
---
¿Cómo puede el álgebra lineal ayudar a optimizar una función no-lineal?

---

La loss `L(w) = ||Aw-b||²` (usada en el lab de ML de Cap 8.4) es cuadrática — no-lineal — pero tiene una estructura especial: es exactamente el fire-engine problem generalizado a varios vectores (el punto en el span de las columnas de A más cercano a b). Se resuelve EXACTO con orthogonality/projection (Cap 9, generalización de `project_along`), sin necesidad de iterar con gradient descent. Gradient descent es genérico (sirve para cualquier función), pero para esta forma particular hay un atajo directo vía álgebra lineal.

Ref: `02-Topics/Coding-the-Matrix-Inner-Product.md — 8.4.4 — Loss function`
