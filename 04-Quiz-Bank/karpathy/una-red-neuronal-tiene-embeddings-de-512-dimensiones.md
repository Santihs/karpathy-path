---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - duality
  - cross-product
noteId: 1785651974975
---
Una red neuronal tiene embeddings de 512 dimensiones. ¿Cómo uses dot product para medir similitud entre dos embeddings?

---

Normaliza ambos (hazlos unitarios), luego dot product = cos(θ). Resultado cercano a 1 = similares. Cercano a 0 = independientes. Cercano a -1 = opuestos. Cosine similarity = (v·w) / (|v| × |w|).
