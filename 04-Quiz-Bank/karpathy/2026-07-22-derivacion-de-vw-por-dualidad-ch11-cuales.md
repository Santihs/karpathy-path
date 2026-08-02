---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - duality
  - cross-product
noteId: 1785651973793
---
(2026-07-22) Derivación de v×w por dualidad (ch11): ¿cuáles son los 4 pasos, en orden?

---

1) Definir f([x,y,z])=det([x,v,w]) — función de volumen 3D→1D, v,w fijos. 2) Es lineal → por dualidad existe vector dual p único tal que f([x,y,z])=p·[x,y,z] para todo [x,y,z]. 3) Resolver p igualando coeficientes (x,y,z) entre p1x+p2y+p3z y la expansión del determinante → da la fórmula del cross product. 4) Interpretar geométricamente: p tiene longitud=área del paralelogramo(v,w) y dirección perpendicular a ese plano — consecuencia del resultado, no ingrediente del cálculo.
