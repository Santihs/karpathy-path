---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
noteId: 1786916857448
---
¿Qué significa cada parte de "i.i.d." (independent and identically distributed), y por qué es un supuesto tan usado en ML?

---

"Independent": los samples no se influyen entre sí (uno no cambia la probabilidad de otro). "Identically distributed": todos los samples vienen de la misma distribución subyacente (no mezclaste datasets con distribuciones distintas sin avisarle al modelo). Es el supuesto base de casi todo entrenamiento en ML porque permite tratar el dataset completo como muestras intercambiables de una única distribución que el modelo intenta aprender.

Ref: `02-Topics/Probability-Fundamentals.md — 16. Statistical independence, i.i.d., conditional independence`
