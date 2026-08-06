---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - coding-the-matrix
  - klein
  - dimension
self-explain: true
noteId: 1785990658392
---
¿Qué dice el Dimension Principle (D1 y D2), y por qué D2 es tan útil en la práctica?

---

Si V es subespacio de W: (D1) dim V ≤ dim W siempre, y (D2) si además dim V = dim W, entonces V = W exactamente. D2 es útil porque evita verificar vector por vector si dos espacios coinciden — basta con contar dimensiones. Ejemplo: si Span{[1,2],[2,1]} tiene dim 2 (independientes) y R² también tiene dim 2, automáticamente son el mismo espacio sin más chequeo.

Ref: `02-Topics/Coding-the-Matrix-Basis.md — 9. Dimensión y Rank`
