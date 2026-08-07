---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - duality
  - cross-product
noteId: 1786138502081
---
En la derivación de v×w por dualidad (Ch11), ¿qué función f(x) se define para arrancar, y por qué esa elección da un escalar?

---

f(x) = det([x,v,w]) — poner x como primera columna del determinante 3×3 (con v,w fijas). Es lineal en x, y un determinante siempre devuelve un número → f(x) es escalar.

Ref: `02-Topics/Linear-Algebra-Basics.md — Ch 11 — Cross Product como Dualidad`
