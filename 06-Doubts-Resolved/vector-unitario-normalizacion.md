---
tags: [phase-0, linear-algebra, vectors, normalization]
date_resolved: 2026-07-22
---

# Vector unitario y no-unitario — normalización

## Pregunta
¿Qué es un vector unitario vs no-unitario? Necesitaba repaso durante el rewatch de 3B1B ch9 (dualidad) — û aparece como pieza clave y no tenía el concepto firme.

## Respuesta

**Vector unitario** = vector de longitud (norma) exactamente 1. Se escribe con "sombrero": û.

**Vector no-unitario** = cualquier vector con longitud ≠ 1.

**Normalizar** = convertir un vector no-unitario en unitario, dividiendo cada entrada por su norma:

```
û = u / ‖u‖
```

Ejemplo: u=[3,4] → ‖u‖ = √(3²+4²) = 5 → û = [3/5, 4/5] — misma dirección, longitud 1.

## Por qué importa en dualidad (ch9)

Cuando 3B1B pregunta "¿dónde aterrizan î y ĵ?" usando û, que sea unitario es lo que hace que la proyección de î y ĵ sobre la recta de û dé *directamente* las 2 entradas de la matriz 1×2 — sin ningún factor de escala extra distorsionando el resultado. Si se usara un vector no-unitario, la proyección se escalaría por su longitud y la equivalencia matriz-vector ⇔ dot-product dejaría de ser tan limpia (habría que dividir por la norma para recuperarla). Ver [[dot-product-duality-explained]].

## Fuentes
- [Unit vector — Wikipedia](https://en.wikipedia.org/wiki/Unit_vector)
- [Normalization | Introduction to Linear Algebra — FreeText Library](https://www.freetext.org/Introduction_to_Linear_Algebra/Basic_Vector_Operations/Normalization/)
