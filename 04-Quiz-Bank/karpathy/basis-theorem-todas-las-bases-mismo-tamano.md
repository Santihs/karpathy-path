---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - coding-the-matrix
  - klein
  - dimension
self-explain: true
noteId: 1785990658372
---
¿Qué dice el Basis Theorem (Klein 6.1.2) y por qué se deduce directo del Morphing Lemma? Explicá el argumento completo.

---

Todas las bases del mismo espacio vectorial tienen el mismo tamaño. Se prueba aplicando el Morphing Lemma (|S|≥|B| cuando S genera y B es independiente) dos veces cruzado: con B1 como generador y B2 como independiente da |B1|≥|B2|; al revés da |B2|≥|B1|. Las dos desigualdades juntas fuerzan |B1|=|B2|. Es lo que hace que "dimensión" sea un concepto bien definido, no dependiente de qué base elegiste.

Ref: `02-Topics/Coding-the-Matrix-Basis.md — 8. Morphing Lemma y Basis Theorem`
