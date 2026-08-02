---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785651973644
---
`equal()` en `Vec` compara con `==` exacto, entrada por entrada. ¿Qué debilidad tiene esto con floats, y por qué NO se arregla poniendo tolerancia dentro de `equal()`?

---

`0.1+0.2 != 0.3` exacto en floats (error de redondeo acumulado) — vectores matemáticamente iguales comparan distintos. No se arregla con tolerancia dentro de `equal()` porque esa misma función debe seguir siendo EXACTA para fields como GF(2)/int, donde tolerancia rompería la corrección. La solución (Klein) es un helper separado (`is_almost_zero`) aplicado en el call site, no dentro de `__eq__`.
