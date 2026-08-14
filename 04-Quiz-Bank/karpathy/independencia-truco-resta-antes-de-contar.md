---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - coding-the-matrix
  - klein
noteId: 1785990658488
---
V=Span{[1,1,0],[0,1,1],[1,0,-1]}. ¿Son independientes los 3 vectores? (Gap propio 2026-08-06: asumí independencia sin chequear.)

---

No — v1−v2 = [1,1,0]−[0,1,1] = [1,0,−1] = v3 exactamente. v3 es combinación de los otros dos → dependientes → dim V=2, no 3.

Ref: `02-Topics/Coding-the-Matrix-Basis.md — 15. Ejercicios de práctica`
