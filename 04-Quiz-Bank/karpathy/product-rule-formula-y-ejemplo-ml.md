---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857581
---
¿Cuál es la fórmula del product rule y qué clasificador de ML lo usa directo?

---

p(x,y) = p(y|x)*p(x) = p(x|y)*p(y) — toda joint distribution se puede factorizar como marginal x conditional. Naive Bayes lo usa directo: p(clase, features) = p(features|clase) * p(clase).

Ref: `02-Topics/Probability-Fundamentals.md — 10. Sum Rule, Product Rule y Bayes' Theorem`
