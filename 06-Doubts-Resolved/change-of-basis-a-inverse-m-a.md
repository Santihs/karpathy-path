---
tags: [phase-0, linear-algebra, change-of-basis, transformations]
date_resolved: 2026-07-28
---

# Change of basis: por qué grid y language van en direcciones opuestas, y qué hace el sandwich A⁻¹MA

## Pregunta
Confusión con la matriz de cambio de base A (3B1B ch13, ejemplo de la base de "Jennifer" b1=[2,1], b2=[-1,1]): ¿en qué dirección traduce A? Y con el sandwich de 3 matrices A⁻¹MA que aparece al final del capítulo — "necesito más explicación de esto".

## Respuesta

**Dirección de A.** A = matriz cuyas columnas son los vectores base de Jennifer, escritos en nuestro lenguaje. Multiplicar A por un vector dado en coordenadas de Jennifer devuelve ese mismo vector en nuestras coordenadas — **A traduce Jennifer→nosotros**. A⁻¹ hace lo inverso: nosotros→Jennifer.

**Grid vs. Language (la parte contraintuitiva, confirmada por la fuente oficial):**
> "Geometrically this matrix transforms our grid into Jennifer's grid, yet numerically it's translating a vector described in her language to our language." — 3Blue1Brown

Geométricamente A mueve la grilla nuestra hacia la grilla de Jennifer. Numéricamente A traduce el lenguaje de Jennifer al nuestro. Direcciones opuestas del mismo A — no es un error de la explicación, es así como funciona la relación entre "mover ejes" y "traducir números".

**El sandwich A⁻¹MA.** M es una transformación que solo "entiende" nuestro lenguaje (ej. rotar 90° en nuestras coordenadas). Para aplicar esa rotación a un vector v_J dado en coordenadas de Jennifer:

1. `A · v_J` → traduce v_J a nuestro lenguaje
2. `M · (A·v_J)` → aplica la rotación (M solo sabe hablar nuestro idioma)
3. `A⁻¹ · (M·A·v_J)` → traduce el resultado de vuelta al idioma de Jennifer

`A⁻¹MA` completo = la misma transformación M, pero descrita en el idioma de Jennifer — toma un vector en su lenguaje y devuelve el vector transformado, también en su lenguaje.

Cita textual verificada:
> "In general, whenever you see an expression like A⁻¹MA, it suggests a mathematical sort of empathy. The middle matrix represents a transformation as you see it, the outer two matrices represent the empathy, this shift in perspective, and the full matrix product represents that same transformation as someone else sees it." — 3Blue1Brown

## Fuentes
- [Change of basis | 3Blue1Brown](https://www.3blue1brown.com/lessons/change-of-basis/)
- [Change of basis | Essence of linear algebra, chapter 13 — YouTube](https://www.youtube.com/watch?v=P2LTAUO1TdA)
