---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - orthogonality
  - projection
self-explain: true
noteId: 1786163376001
---
¿Cómo se encuentra la proyección de b ortogonal a v?

---

`b^⊥v = b - b^||v`, donde `b^||v = σv` y `σ = <b,v>/<v,v>` (se despeja de exigir que `<b-σv, v> = 0`). Código: `project_orthogonal_1(b,v) = b - project_along(b,v)`.

Ref: `02-Topics/Coding-the-Matrix-Inner-Product.md — 8.3.4 — Cómo calcular σ`
