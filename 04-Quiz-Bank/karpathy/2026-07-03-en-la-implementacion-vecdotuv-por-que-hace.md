---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785651973545
---
En la implementación `Vec.dot(u,v)`, ¿por qué hace falta `assert u.D == v.D` antes de sumar, en vez de solo iterar `zip(u.f, v.f)`?

---

`u.f`/`v.f` son dicts sparse — pueden tener distintas claves presentes (ausente = 0 implícito). `zip` sobre los dicts sparse desalinearía o saltearía entradas. Hay que iterar sobre el domain declarado `D`, no sobre el storage sparse.

Ref: `05-Projects/coding-the-matrix/src/coding_the_matrix/vec.py`
