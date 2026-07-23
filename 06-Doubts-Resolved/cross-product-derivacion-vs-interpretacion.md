---
tags: [phase-0, linear-algebra, cross-product, duality]
date_resolved: 2026-07-22
---

# Cross product: derivación por dualidad vs. lectura geométrica "área × perpendicular"

## Pregunta
"si tomamos el área del paralelogramo y multiplicamos por el perpendicular al paralelogramo, ¿entonces encontramos otro vector paralelo al área del paralelogramo?" — confusión sobre si v×w se CONSTRUYE multiplicando área por un vector perpendicular.

## Respuesta

No. v×w no se construye multiplicando área por perpendicular — se **deriva** resolviendo una ecuación de dualidad. Área y perpendicularidad son la lectura geométrica del resultado, no ingredientes del cálculo.

**Derivación real (4 pasos):**

1. Se define f([x,y,z]) = det([x,v1,w1 / y,v2,w2 / z,v3,w3]) — función 3D→1D (volumen con signo del paralelepípedo), v y w fijos.
2. Es lineal → por dualidad (ch9) existe un único vector p tal que f([x,y,z]) = p·[x,y,z] para TODO [x,y,z].
3. Se resuelve p igualando coeficientes entre p1x+p2y+p3z y la expansión del determinante → p1=v2w3-v3w2, p2=v3w1-v1w3, p3=v1w2-v2w1 — exactamente la fórmula del cross product.
4. **Recién después** de tener p, se interpreta geométricamente: para que p·[x,y,z] dé el volumen del paralelepípedo (=área base v,w × altura de [x,y,z] perpendicular al plano), p necesariamente tiene que tener longitud=área del paralelogramo(v,w) y dirección perpendicular a ese plano. Eso no es un paso del cálculo — es la única forma geométrica en que la ecuación de dualidad puede cumplirse.

**Corrección de precisión adicional:** p es perpendicular al **plano formado por v,w** (2D, el paralelogramo base), no al paralelepípedo completo (un sólido 3D no tiene una única dirección perpendicular). El paralelepípedo es la figura que se forma entre el vector variable de entrada y v,w — su volumen es lo que p·[x,y,z] calcula.

Ver derivación visual completa en [[cross-product-duality-derivation-2026-07-22]] (07-Visuals).

## Fuentes
- [Cross products in the light of linear transformations | Chapter 11, Essence of linear algebra — 3Blue1Brown (YouTube)](https://www.youtube.com/watch?v=BaM7OCEm3G0)
