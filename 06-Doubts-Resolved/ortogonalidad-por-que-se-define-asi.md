---
tags: [phase-0, coding-the-matrix, orthogonality]
date: 2026-08-10
---

# Ortogonalidad: por qué `<u,v>=0` y no otra condición

## La pregunta

¿Por qué "ortogonal" se define como `<u,v> = 0`? ¿Es arbitrario o hay una razón?

## Derivación

Para cualquier par de vectores `u`, `v`, expandiendo el producto interno del vector suma:

```
||u+v||² = <u+v, u+v> = <u,u> + 2<u,v> + <v,v> = ||u||² + 2<u,v> + ||v||²
```

Pitágoras real (triángulo rectángulo) dice `||u+v||² = ||u||² + ||v||²` — SIN el término cruzado `2<u,v>`.

Las dos ecuaciones solo coinciden cuando `2<u,v> = 0`, o sea `<u,v> = 0`.

**Conclusión:** "ortogonal" no es una definición arbitraria — es la condición exacta y única que hace desaparecer el término cruzado y hace que Pitágoras valga.

## Ejemplos numéricos

**Caso ortogonal**, `v=(3,0)`, `u=(0,2)`:
```
<u,v> = 0*3 + 2*0 = 0        → ortogonales
||u+v||² = ||(3,2)||² = 13
||u||² + ||v||² = 4 + 9 = 13  → coincide, Pitágoras exacto
```

**Caso NO ortogonal**, `u=(1,1)`, `v=(3,0)`:
```
<u,v> = 3 ≠ 0
||u+v||² = ||(4,1)||² = 17
||u||²+||v||² = 2+9 = 11       → NO coincide
diferencia = 6 = 2<u,v>        → exactamente el término cruzado que falta
```

## Para qué sirve saber esto (no es solo teoría)

1. **Proyección ortogonal / fire-engine problem (Cap 8-9):** encontrar el punto más cercano a `b` dentro de un span (o de una recta `Span{v}`) se resuelve exigiendo que el "resto" `b - σv` sea ortogonal a `v`. Sin la definición `<u,v>=0` no hay forma de plantear esa ecuación y despejar `σ`.

2. **Gram-Schmidt / QR factorization (Cap 9.3):** el algoritmo entero consiste en ir restando proyecciones para que cada vector nuevo quede ortogonal a los anteriores. Sirve para tener una base "limpia" donde cada eje es independiente de los demás — sin superposición de información.

3. **Least-squares / regresión lineal (Cap 9.9, ML lab Cap 8.4):** ajustar una recta/modelo a datos con ruido (`L(w) = ||Aw-b||²`) es exactamente el fire-engine problem generalizado — se resuelve EXACTO vía ortogonalidad, sin iterar con gradient descent. Es la base matemática detrás de `np.linalg.lstsq` y de por qué la regresión lineal tiene solución cerrada.

4. **Compresión / PCA / bases ortonormales:** cuando una base es ortogonal, las coordenadas de un vector en esa base se calculan por proyección simple (`<b,v_i>` en vez de resolver un sistema lineal completo) — mucho más barato computacionalmente. Por eso JPEG, PCA, y las redes que usan bases ortogonales (ej. algunos esquemas de attention/positional encoding) explotan esta propiedad.

5. **Intuición general de ML:** features/dimensiones ortogonales = información no redundante entre sí. Cuando dos direcciones NO son ortogonales, hay "solapamiento" (correlación) — el término cruzado `2<u,v>` mide justo esa redundancia.

Ref: `02-Topics/Coding-the-Matrix-Inner-Product.md — 8.3 — Orthogonality`
