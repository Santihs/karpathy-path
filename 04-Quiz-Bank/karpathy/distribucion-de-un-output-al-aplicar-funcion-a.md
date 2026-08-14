---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
self-explain: true
noteId: 1786682559951
---
¿Cómo se calcula la distribución del output al aplicar una función a una random variable? Da el patrón de código.

---

groupby + sum: por cada outcome, sumás su probabilidad al bucket de `f(outcome)`. `out[f(outcome)] += p` para cada `(outcome, p)` del dict original. Si dos outcomes distintos caen en el mismo output, sus probabilidades se suman ahí.

Ref: `02-Topics/Probability-Fundamentals.md — Parte 1, sección 3`
