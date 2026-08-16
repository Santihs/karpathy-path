---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857547
---
En una pmf (discreto) la altura de la barra ES la probabilidad. En una pdf (continuo), ¿qué es la altura y por qué puede superar 1?

---

Es densidad, no probabilidad. Solo el ÁREA bajo la curva (integral) tiene que sumar 1 — la altura en un punto puede ser cualquier valor no-negativo, incluso >1, mientras el área total se mantenga en 1. Por eso P(X=punto exacto)=0 en continuo: un punto no tiene ancho, así que su área es cero sin importar la altura.

Ref: `02-Topics/Probability-Fundamentals.md — 9. Continuous probabilities — pdf y cdf`
