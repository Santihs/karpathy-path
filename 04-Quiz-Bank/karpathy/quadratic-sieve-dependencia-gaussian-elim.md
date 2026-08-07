---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - gaussian-elimination
  - gf2
  - rsa
self-explain: true
noteId: 1786146122052
---
En el quadratic sieve, ¿por qué está garantizada una dependencia lineal entre los vectores, y qué hace Gaussian elimination con ella?

---

Con K+1 vectores en un espacio de dimensión K=len(primeset), son necesariamente dependientes (Dimension Principle). Gaussian elimination sobre GF(2) encuentra la combinación de filas que suma cero, es decir, el producto de esos (x²-N) tiene todos los exponentes pares → es un cuadrado perfecto b².

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.6-7.8 — Factoring integers (RSA, quadratic sieve)`
