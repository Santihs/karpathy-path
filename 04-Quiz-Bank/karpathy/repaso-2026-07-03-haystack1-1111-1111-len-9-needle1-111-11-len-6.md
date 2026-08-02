---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - coding-the-matrix
  - klein
noteId: 1785651974793
---
(repaso 2026-07-03) haystack=[1,-1,1,1,1,-1,1,1,1] (len 9), needle=[1,-1,1,1,-1,1] (len 6). Sin mirar la nota: ¿cuántas posiciones de inicio hay, y cuánto da el dot-product en pos 0?

---

Posiciones = 9-6+1 = 4 (0,1,2,3). Pos 0: [1,-1,1,1,1,-1]·needle = 1+1+1+1-1-1 = 2. Resultado completo: [2,2,0,0].
