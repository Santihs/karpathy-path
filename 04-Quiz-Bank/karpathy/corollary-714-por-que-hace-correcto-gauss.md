---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - gaussian-elimination
  - duality
self-explain: true
noteId: 1786146121876
---
¿Por qué el Corollary 7.1.4 (Row(MA)=Row(A) si M invertible) es lo que hace correcto a Gaussian elimination?

---

Cada row-addition operation equivale a multiplicar por una matriz invertible. Por el corollary, ninguna de esas operaciones cambia el row space — solo la forma en que se expresa. Por eso la base que sale al final de la reducción sigue siendo base del row space ORIGINAL.

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.1.5-7.1.6 — Por qué el algoritmo es correcto`
