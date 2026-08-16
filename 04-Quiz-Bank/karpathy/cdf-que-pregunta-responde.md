---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857146
---
¿Qué pregunta responde el cdf que el pdf no puede responder directo, y cómo se relacionan?

---

cdf F_X(x) = P(X<=x) — probabilidad acumulada hasta un punto (la única forma de sacar probabilidad REAL de una variable continua, ya que P(X=x exacto)=0). Se calcula integrando el pdf desde -infinito hasta x. Ejemplo dev: percentiles de latencia (p50, p99) son literal un cdf invertido.

Ref: `02-Topics/Probability-Fundamentals.md — 9. Continuous probabilities — pdf y cdf`
