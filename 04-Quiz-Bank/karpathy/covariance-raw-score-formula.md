---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857316
---
¿Cuál es la raw-score formula de la covarianza (la que se usa para calcular en la práctica)?

---

Cov[x,y] = E[xy] - E[x]*E[y] ("expected value del producto, menos producto de expected values"). Es la que se usa en la práctica: se deriva por linealidad de la definición estándar Cov[x,y]=E[(x-E[x])(y-E[y])].

Ref: `02-Topics/Probability-Fundamentals.md — 12. Covariance, variance, covariance matrix, correlation`
