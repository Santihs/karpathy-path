---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785651974363
---
¿Por qué el dot-product con all-ones sobre GF(2) es la base de un parity bit / checksum?

---

Porque detecta si la cantidad de 1s cambió de paridad — si un bit se corrompe en transmisión, la paridad calculada ya no coincide con la esperada, señal de error. Base de ECC memory, RAID, checksums de red.

Ref: `02-Topics/Coding-the-Matrix-Vectors.md — 11. Dot-product sobre GF(2)`
