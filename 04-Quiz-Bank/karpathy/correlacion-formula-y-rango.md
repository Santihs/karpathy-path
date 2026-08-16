---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857214
---
¿Cuál es la fórmula de la correlación y por qué hace falta normalizar la covarianza para obtenerla?

---

corr[x,y] = Cov[x,y] / sqrt(V[x]*V[y]), siempre en [-1,1]. La covarianza sola depende de las escalas de x e y (unidades distintas dan magnitudes raras) — dividir por las desviaciones estándar de cada variable normaliza esa dependencia de escala, dejando un número comparable entre cualquier par de variables.

Ref: `02-Topics/Probability-Fundamentals.md — 12. Covariance, variance, covariance matrix, correlation`
