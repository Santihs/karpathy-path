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
haystack=[1,1,-1,-1,1,-1,1,-1] (len 8), needle=[1,-1,-1,1] (len 4). Sin mirar la nota: ¿cuántas posiciones de inicio hay, y cuánto da el dot-product en pos 0?

---

Posiciones = 8-4+1 = 5 (0,1,2,3,4). Pos 0: [1,1,-1,-1]·[1,-1,-1,1] = 1-1+1-1 = 0. Resultado completo: [0,4,-2,0,0] — match perfecto en pos 1 (valor=4=len(needle)).

Ref: `02-Topics/Coding-the-Matrix-Fundamentals.md — 10. Cap 4.6 — Needle-in-haystack como matrix-vector (4.6.6)`
