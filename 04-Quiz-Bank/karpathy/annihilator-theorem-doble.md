---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - coding-the-matrix
  - klein
  - annihilator
self-explain: true
noteId: 1785990658340
---
¿Qué dice el Annihilator Theorem, (V°)°=V, y cómo se prueba usando el Annihilator Dimension Theorem?

---

El annihilator del annihilator es el espacio original: (V°)°=V. Prueba: cada vector base de V está en (V°)° por definición cruzada de perpendicularidad, así que V es subespacio de (V°)°. Falta igualar dimensiones: por el Annihilator Dimension Theorem (dim V+dim V°=n) aplicado dos veces —a V y a V°— y restando, sale dim V=dim(V°)°. Por Dimension Principle (D2), mismo subespacio + misma dimensión → son iguales.

Ref: `02-Topics/Coding-the-Matrix-Basis.md — 12. El Annihilator`
