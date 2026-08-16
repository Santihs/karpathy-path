---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857717
---
¿Cuál es la raw-score formula de la varianza y por qué permite calcularla en una sola pasada por los datos (a diferencia de la definición estándar)?

---

V[x] = E[x^2] - (E[x])^2 ("mean del cuadrado, menos cuadrado de la mean"). La definición estándar V[x]=E[(x-mu)^2] necesita conocer mu ANTES de calcular las desviaciones (2 pasadas: una para mu, otra para la varianza). La raw-score formula solo necesita acumular sum(x) y sum(x^2) simultáneamente en una sola pasada — aunque puede ser numéricamente inestable si ambos términos son grandes y casi iguales.

Ref: `02-Topics/Probability-Fundamentals.md — 14. Tres expresiones de la varianza`
