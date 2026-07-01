---
tags: [phase-0, linear-algebra, cross-product]
date_resolved: 2026-06-30
---

# ¿Para qué sirve el cross product? (mundo real y ML)

## Mundo real

1. **Gráficos 3D — normales de superficie**: v×w de dos aristas de un triángulo da vector perpendicular a la superficie. Usado para iluminación y sombreado (Unity, Blender, OpenGL).
2. **Física — torque**: τ = r × F. Fuerza a distancia r del pivote → torque perpendicular, define eje de rotación.
3. **Robótica**: cinemática, orientación de brazos, planeación de movimiento.
4. **Detección de colisión / intersección de polígonos** en gráficos y visión computacional.

## En ML — uso limitado (a diferencia del dot product)

Dot product está en todas partes en ML (attention, similitud coseno, cada neurona `w·x`). Cross product **no** — solo existe en 3D, y ML mayormente opera en espacios de alta dimensión.

Dónde sí aparece:
- Visión computacional 3D / point clouds: normales de superficie (LiDAR, self-driving, reconstrucción 3D)
- RL con simulación física: motor de física usa cross product para torque/momento angular
- Gráficos generativos 3D (NeRF, mallas): cálculo de normales

**Trampa común:** "cross product" en papers de ML tabular frecuentemente se refiere a **feature crossing** (combinar features categóricas) — término no relacionado al cross product vectorial.

## Fuentes
- [The Right-Hand Rule: Why Physics and 3D Graphics Both Need a Perpendicular Vector](https://www.mathisimple.com/calculator/articles/cross-product-right-hand-rule)
- [Automatically Learning Feature Crossing from Model Interpretation for Tabular Data](https://openreview.net/forum?id=Sye2s2VtDr)
