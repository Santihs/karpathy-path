---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - coding-the-matrix
  - klein
  - kernel-image
self-explain: true
noteId: 1785990658574
---
Enunciá el Kernel-Image Theorem y explicá la idea intuitiva de por qué es cierto (sin la prueba formal completa).

---

dim(Ker f) + dim(Im f) = dim(dominio de f). Intuición: cada dimensión del dominio o "sobrevive" en la imagen, o se pierde en el kernel (lo que f manda a cero) — no hay tercera opción, y f no puede crear ni destruir dimensiones de la nada. Se prueba formalmente mostrando que el dominio V se descompone como Ker(f) ⊕ V* (una subfunción invertible construida a partir de f), y aplicando la fórmula de dimensión del direct sum.

Ref: `02-Topics/Coding-the-Matrix-Basis.md — 11. Dimension y funciones lineales — Kernel-Image Theorem`
