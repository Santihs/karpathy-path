---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - gaussian-elimination
  - gf2
  - rsa
self-explain: true
noteId: 1786146122111
---
En el quadratic sieve, una vez encontrado el cuadrado perfecto b², ¿cómo se obtiene un divisor de N?

---

Sea a el producto de los x usados: a²-b²=kN. Calculando gcd(a-b, N) se obtiene, con suerte, un divisor no-trivial de N.

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.6-7.8 — Factoring integers (RSA, quadratic sieve)`
