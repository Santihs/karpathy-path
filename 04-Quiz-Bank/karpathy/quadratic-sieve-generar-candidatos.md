---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - gaussian-elimination
  - gf2
  - rsa
self-explain: true
noteId: 1786146122078
---
En el quadratic sieve, ¿cómo se generan los candidatos y cómo se codifican como vectores en GF(2)?

---

Se generan x tales que x²-N factoriza completamente sobre un conjunto chico de primos (primeset). Cada factorización se codifica como vector en GF(2) marcando la PARIDAD de cada exponente.

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.6-7.8 — Factoring integers (RSA, quadratic sieve)`
