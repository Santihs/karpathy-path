---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857516
---
¿Por qué la mediana es más robusta a outliers que la media, y qué ejemplo dev usa literal el concepto de mediana?

---

La media pondera TODOS los valores (un outlier extremo la arrastra); la mediana solo mira el valor del medio (50% arriba, 50% abajo del cdf), así que un valor raro no cambia dónde está "el medio". Ejemplo dev: p50 de latencia (percentil 50) ES la mediana — si un request tarda 60s por timeout raro, la mediana ni se entera, pero la media se dispara.

Ref: `02-Topics/Probability-Fundamentals.md — 11. Expected value, mean, median, mode`
