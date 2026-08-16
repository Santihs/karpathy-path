---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857413
---
¿En qué se diferencia E[X] de un promedio simple (sum(valores)/N), y cuándo coinciden?

---

E[X] = sum(valor * probabilidad) — cada valor pesa según su probabilidad, no por igual (1/N). El promedio simple asume implícitamente que todos los outcomes son igual de probables. Solo coinciden cuando la distribución es uniforme. La media (Definition 6.4) es el caso especial de expected value donde g=identidad.

Ref: `02-Topics/Probability-Fundamentals.md — 11. Expected value, mean, median, mode`
