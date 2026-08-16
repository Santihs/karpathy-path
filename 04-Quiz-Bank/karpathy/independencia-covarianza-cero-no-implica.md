---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
self-explain: true
noteId: 1786916857483
---
¿Cuál es la definición formal de independencia estadística, y por qué covarianza=0 NO implica independencia? Dá el contraejemplo del libro.

---

X,Y independientes ssi p(x,y)=p(x)p(y) — el joint se factoriza limpio, sin necesidad de conditional. Si independientes: p(y|x)=p(y), Cov[x,y]=0.

El recíproco NO vale: covarianza solo mide dependencia LINEAL. Contraejemplo (Example 6.5): X con media 0 y E[x^3]=0, Y=x^2 — Y depende 100% de X (es una función exacta), pero Cov[x,y]=E[xy]-E[x]E[y]=E[x^3]=0 pese a la dependencia clara, porque la relación es cuadrática (no-lineal), y la covarianza no la detecta.

Ref: `02-Topics/Probability-Fundamentals.md — 16. Statistical independence, i.i.d., conditional independence`
