---
tags: [phase-0, linear-algebra, coding-the-matrix, span, basis]
date_resolved: 2026-07-17
---

# ¿Qué es el "span" de un conjunto de vectores?

**Definición:** el span de `{a1,...,an}` es el conjunto de TODAS las combinaciones lineales posibles de esos vectores — todo lo que `α1*a1 + α2*a2 + ... + αn*an` puede llegar a dar, variando los escalares `α`. Es el subespacio más chico que contiene a esos vectores.

No es "los vectores en sí" — es el universo entero de resultados alcanzables combinándolos.

## Ejemplo (Klein 5.2.3 — compresión de imágenes)

`a1 = [255,0,255,0]`, `a2 = [0,255,0,255]`. `span{a1,a2}` = todas las imágenes representables como `α1*a1 + α2*a2`. Como `a1` solo tiene valor en posiciones 1,3 y `a2` solo en 2,4, cualquier combinación mantiene **la misma proporción** entre posiciones 1-3 y entre 2-4. Por eso `[255,200,150,90]` queda fuera del span — sus proporciones no calzan con ningún `α1,α2`.

**Intuición geométrica:** 2 generadores no-paralelos en 2D tienen span = todo el plano. Pero en `R⁴` (4 píxeles), 2 generadores solo cubren un "plano" chico dentro de un espacio mucho más grande — la mayoría de los puntos de `R⁴` quedan afuera. Esto motiva la pregunta de cuántos generadores hacen falta para que el span cubra el espacio entero (Klein Question 5.2.4/5.2.5 → tema de basis/dimensión).

## Fuentes
- [Linear span - Wikipedia](https://en.wikipedia.org/wiki/Linear_span)
- [Linear combinations, span, and basis vectors — 3Blue1Brown](https://www.3blue1brown.com/lessons/span/)
