---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857677
---
¿Cuál es la fórmula de V[X+Y], y qué pasa si X e Y están correlacionadas positivamente?

---

V[X+Y] = V[X] + V[Y] + 2*Cov[X,Y]. Si están correlacionadas positivamente, Cov[X,Y]>0, así que V[X+Y] es MAYOR que la simple suma de varianzas — se amplifican mutuamente. Si no están correlacionadas (Cov=0), se reduce al Pitágoras simple V[X+Y]=V[X]+V[Y].

Ref: `02-Topics/Probability-Fundamentals.md — 15. Sums y transformaciones afines de random variables`
