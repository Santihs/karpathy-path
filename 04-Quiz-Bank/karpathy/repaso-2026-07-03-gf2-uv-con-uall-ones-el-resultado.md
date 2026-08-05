---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785651974775
---
GF(2), u·v con u=all-ones. El resultado es 0 o 1 — ¿pero qué SIGNIFICA ese valor?

---

No es solo "0 o 1" trivial de GF(2) — significa la PARIDAD de v (par/impar cantidad de 1s). Ese significado es lo que lo hace útil como parity bit/checksum: detecta cambio de paridad = bit corrupto.

Ref: `02-Topics/Coding-the-Matrix-Vectors.md — 11. Dot-product sobre GF(2)`
