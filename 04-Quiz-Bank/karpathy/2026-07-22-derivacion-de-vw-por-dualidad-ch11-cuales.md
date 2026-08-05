---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - duality
  - cross-product
noteId: 1785651973793
self-explain: true
---
En la derivación de v×w por dualidad (ch11), ¿por qué necesitás que f([x,y,z])=det([x,v,w]) sea LINEAL para poder aplicar el paso de dualidad?

---

Porque el teorema de dualidad (Riesz-tipo, dim finita) solo garantiza la existencia de un vector dual único p tal que f(x)=p·x cuando f es una función lineal escalar. Si f no fuera lineal, no habría garantía de que exista tal p — la linealidad de f (det es lineal en cada fila fija las otras) es la condición que habilita el paso 2 de la derivación.

Ref: `02-Topics/Linear-Algebra-Basics.md — Ch 11 — Cross Product como Dualidad`
