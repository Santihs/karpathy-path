---
tags: [phase-0, coding-the-matrix, basis, span, errata]
date_resolved: 2026-07-18
---

# Klein Example 5.3.2 — "Span B = R³" es una errata del libro

## La duda

En el Shrink algorithm example (Cap 5.3.2, pág. 276), Klein da:

```
v1 = [1, 0, 0]
v2 = [0, 1, 0]
v3 = [1, 2, 0]
v4 = [3, 1, 0]
```

Después de sacar v4 (=3v1+v2) y v3 (=v1+2v2), el texto dice:

> "Finally, note that Span B = R³ and that neither v1 nor v2 alone could generate R³."

## Verificación

Verificado contra el PDF fuente directamente (`00-Meta/resources/Philip N. Klein-...pdf`, línea 16296 del texto extraído) — la cita es exacta, no es error de transcripción/OCR.

Matemáticamente: los 4 vectores dados tienen tercera coordenada (z) siempre 0. Cualquier combinación lineal de v1..v4 también tiene z=0 (0 es cerrado bajo suma y escalado). Por lo tanto:

```
Span({v1,v2,v3,v4}) = {(a,b,0) : a,b ∈ R}  — el plano xy, subespacio 2D de R³
```

Esto NUNCA puede ser R³ completo (que necesita también vectores con z≠0, ej. [0,0,1]). El texto del libro es inconsistente con los propios datos que da.

## Por qué no rompe el argumento del ejemplo

El punto pedagógico del ejemplo (Shrink saca v4 y v3 por ser redundantes, y v1,v2 quedan porque ninguno solo puede generar al otro) sigue siendo correcto — solo hay que leer "Span B = R³" como "Span B = R² (embebido como plano z=0 dentro de R³)", no como R³ literal. Es un lapsus del autor al escribir el ejemplo, no un error en la lógica del algoritmo Shrink.

## Fuentes
- Klein, *Coding the Matrix* (2013), Cap 5.3.2, pág. 276 — Example 5.3.2 (verificado línea por línea contra el PDF del curso)
