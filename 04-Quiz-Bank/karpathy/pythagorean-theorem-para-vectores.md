---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - orthogonality
  - pythagorean-theorem
self-explain: true
noteId: 1786163376127
---
¿Cuál es el Teorema de Pitágoras para vectores, y por qué la condición es exactamente "ortogonales"?

---

Si `u` es ortogonal a `v`, entonces `||u+v||² = ||u||² + ||v||²`.

Por qué: expandiendo `||u+v||² = <u+v,u+v> = ||u||² + 2<u,v> + ||v||²`. Esto solo coincide con `||u||²+||v||²` (Pitágoras exacto) cuando el término cruzado `2<u,v>` se anula — es decir, cuando `<u,v>=0`. Por eso la definición de "ortogonal" se elige exactamente así: es la condición que hace que Pitágoras valga.

Ref: `02-Topics/Coding-the-Matrix-Inner-Product.md — 8.3 — Orthogonality`
