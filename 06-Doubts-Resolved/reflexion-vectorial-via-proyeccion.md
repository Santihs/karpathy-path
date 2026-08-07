---
tags: [phase-0, linear-algebra, dot-product, reflection]
date_resolved: 2026-08-07
---

# Reflejar un vector = 2×proyección - vector original

## Pregunta
Al reflejar un vector, ¿es producto punto más "mover" el vector sobre lo que queremos reflejar?

## Respuesta

Reflejar w sobre la línea de v: `reflejo = 2·proj_v(w) - w`.

**Derivación:** descomponer w en parte paralela a v (`w∥`) + parte perpendicular (`w⊥`), con `w = w∥ + w⊥`. La proyección escalar/vectorial (ver [[dot-product-duality-explained]]) da exactamente `w∥` — el "pie" de w sobre la línea de v.

Reflejar mantiene `w∥` igual e invierte `w⊥`:
```
reflejo = w∥ - w⊥ = w∥ - (w - w∥) = 2·w∥ - w = 2·proj_v(w) - w
```

Geométricamente: proyectás (llegás al pie sobre la línea), y seguís de largo la misma distancia hacia el otro lado — "el doble de la sombra menos el original".

**Chequeo numérico** (v=[2,0], w=[1,1]): proyección vectorial = comp·v̂ = 1·[1,0] = [1,0]. Reflejo = 2·[1,0] - [1,1] = [1,-1]. Correcto: reflejar [1,1] sobre eje x da [1,-1].

**Nota sobre signo:** la fórmula estándar en gráficos/física es para reflejo sobre la *normal* de una superficie: `R = V - 2·proj_n(V)`. La versión de arriba es la misma idea pero proyectando sobre la *línea* (no la normal) — por eso el signo está invertido (`2·proj - w` en vez de `w - 2·proj`).

## Fuentes
- [Vector reflection at a surface — Sunshine's Homepage](https://www.sunshine2k.de/articles/coding/vectorreflection/vectorreflection.html)
- [11.7 Vector Reflections — Contemporary Calculus](https://www.contemporarycalculus.com/dh/Calculus_all/CC11_7_VectorReflections.pdf)
