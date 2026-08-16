---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
self-explain: true
noteId: 1786916857125
---
Derivá Bayes' theorem a partir del product rule, y nombrá los 4 términos de la fórmula (posterior, likelihood, prior, evidence). ¿Por qué el likelihood NO es una distribución en x?

---

Product rule da 2 formas de escribir la misma joint: p(x,y)=p(x|y)p(y) y p(x,y)=p(y|x)p(x). Igualando y despejando p(x|y): p(x|y) = p(y|x)p(x) / p(y).

- Prior p(x): creencia previa sobre la variable latente x, antes de ver datos.
- Likelihood p(y|x): "prob de los datos y si supiéramos x" — es distribución en y, NO en x (nunca se dice "likelihood de y").
- Evidence p(y): normaliza el posterior, se calcula con sum rule integrando el numerador respecto a x — E_X[p(y|x)].
- Posterior p(x|y): lo que interesa — qué sabemos de x después de observar y.

Ejemplo: filtro de spam, prior 20% salta a posterior 71.4% al observar la palabra "gratis".

Ref: `02-Topics/Probability-Fundamentals.md — 10. Sum Rule, Product Rule y Bayes' Theorem`
