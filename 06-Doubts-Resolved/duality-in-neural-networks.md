---
tags: [phase-0, linear-algebra, duality, dot-product, neural-networks]
date_resolved: 2026-06-30
---

# Cómo funciona duality (ch9) en ML real

Cada neurona en una red: `y = w·x + b`. `w` es el vector dual del funcional lineal que esa neurona representa (dualidad, ch9).

- Toda función lineal nD→1D solo puede tomar la forma `w·x` (dualidad lo garantiza).
- **Entrenar = buscar el vector dual correcto.** Backprop ajusta `w` hasta que `f(x)=w·x` aproxime la función objetivo.
- Interpretación geométrica: neurona mide "cuánto se parece x a la dirección w" — proyección.
- **Attention (Q·Kᵀ)**: mismo mecanismo — proyección de query contra cada key.

Cross product en sí: uso mínimo en ML (solo 3D — gráficos, robótica, RL con física). Ver [[cross-product-real-world-ml-uses]]. Pero duality **como concepto** es la base de por qué toda red neuronal es cascada de productos punto.

## Fuentes
- [Mastering PyTorch Linear Layers: A Comprehensive Guide](https://www.myscale.com/blog/pytorch-linear-layer-data-driven-analysis/)
- [Fully Connected Layer vs. Convolutional Layer: Explained](https://builtin.com/machine-learning/fully-connected-layer)
