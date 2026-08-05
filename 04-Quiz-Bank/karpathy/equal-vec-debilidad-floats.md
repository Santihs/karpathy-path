---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785903292899
---
`equal()` en `Vec` compara con `==` exacto, entrada por entrada. ¿Qué debilidad tiene esto con floats?

---

`0.1+0.2 != 0.3` exacto en floats (error de redondeo acumulado) — vectores matemáticamente iguales comparan distintos.

Ref: `05-Projects/coding-the-matrix/src/coding_the_matrix/vec.py`
