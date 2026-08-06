---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - coding-the-matrix
  - klein
  - direct-sum
noteId: 1785990658438
---
¿Bajo qué condición se puede formar el direct sum U⊕V de dos subespacios? ¿Y qué NO es (con qué no hay que confundirlo)?

---

Solo cuando U y V comparten ÚNICAMENTE el vector cero. Si comparten algo más, es ilegal formar U⊕V. No es lo mismo que la unión de conjuntos U∪V (que solo junta elementos tal cual) — U⊕V = {u+v : u∈U, v∈V}, TODAS las sumas posibles, generalmente mucho más grande que la unión.

Ref: `02-Topics/Coding-the-Matrix-Basis.md — 10. Direct Sum`
