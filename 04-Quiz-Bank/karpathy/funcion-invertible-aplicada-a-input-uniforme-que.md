---
tags:
  - repo-karpathy
  - phase-0
  - probability
  - mml-book
  - crypto
self-explain: true
noteId: 1786682559985
---
Función invertible aplicada a input uniform random — ¿qué pasa con la distribución del output, y por qué importa para crypto (one-time pad)?

---

El output también sale uniforme. Como la función es invertible (bijective), no hay collisions en el groupby — cada output tiene exactamente un input, así que `P(output) = P(su único input)`, no se suma nada. Por eso: key uniforme + encriptación invertible → ciphertext uniforme, sin importar el plaintext — el atacante no gana info mirando el output. Base matemática del one-time pad.

Ref: `02-Topics/Probability-Fundamentals.md — Parte 1, sección 4`
