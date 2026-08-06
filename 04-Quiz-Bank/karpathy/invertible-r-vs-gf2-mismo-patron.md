---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - coding-the-matrix
  - klein
  - gf2
noteId: 1785990658522
---
La matriz [[1,0,1],[0,1,1],[1,1,0]] es invertible sobre R pero NO sobre GF(2), a pesar de tener exactamente el mismo patrón de 0s y 1s. ¿Por qué?

---

Sobre GF(2), fila1+fila2 = [1,1,0] (porque 1+1=0 en GF(2)) — eso es exactamente fila3, así que las filas son dependientes → no invertible. Sobre R, esa misma suma da [1,1,2]≠fila3, no hay dependencia. Invertibilidad depende del CAMPO sobre el que trabajás, no solo de qué números aparecen en la matriz.

Ref: `05-Projects/coding-the-matrix/src/coding_the_matrix/basis.py`
