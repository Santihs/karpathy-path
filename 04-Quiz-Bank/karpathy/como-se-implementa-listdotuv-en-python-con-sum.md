---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785651973893
---
¿Cómo se implementa list_dot(u,v) en Python con sum() + list comprehension?

---

`def list_dot(u, v): return sum([u[i]*v[i] for i in range(len(u))])` — o equivalente con zip: `sum([a*b for (a,b) in zip(u,v)])`.

Ref: `05-Projects/coding-the-matrix/src/coding_the_matrix/vec.py`
