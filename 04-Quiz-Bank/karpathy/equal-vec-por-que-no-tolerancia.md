---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785903292917
---
¿Por qué NO se arregla la debilidad de `equal()` con floats poniendo tolerancia dentro de la función misma?

---

Porque `equal()` debe seguir siendo EXACTA para fields como GF(2)/int, donde tolerancia rompería la corrección.

Ref: `05-Projects/coding-the-matrix/src/coding_the_matrix/vec.py`
