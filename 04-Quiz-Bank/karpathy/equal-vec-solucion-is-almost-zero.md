---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785903292955
---
¿Cuál es la solución de Klein para comparar vectores de floats con tolerancia, sin tocar `equal()`?

---

Un helper separado (`is_almost_zero`) aplicado en el call site, no dentro de `__eq__`.

Ref: `05-Projects/coding-the-matrix/tests/test_vec.py — test_equal_is_exact_and_breaks_on_float_accumulation`
