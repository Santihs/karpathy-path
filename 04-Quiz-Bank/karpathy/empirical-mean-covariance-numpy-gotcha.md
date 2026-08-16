---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857349
---
¿Qué funciones de numpy calculan mean y covariance empíricas, y qué gotcha tiene el default de np.cov respecto a la fórmula del libro (Eq 6.42)?

---

np.mean(X, axis=0) calcula la empirical mean (coincide con Eq 6.41, divide por N). np.cov(X.T) calcula la covariance, pero por default usa ddof=1 (divide por N-1, "unbiased/corrected") — NO la versión "biased" (divide por N) que usa el libro en Eq 6.42. Para replicar Eq 6.42 exacto hay que pasar ddof=0 (o bias=True).

Ref: `02-Topics/Probability-Fundamentals.md — 13. Empirical mean/covariance`
