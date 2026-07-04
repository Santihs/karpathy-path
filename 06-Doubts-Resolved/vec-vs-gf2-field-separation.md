---
tags: [phase-0, coding-the-matrix, vectors, fields, gf2]
date_resolved: 2026-07-03
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Vec vs GF2 — por qué son clases separadas

**Duda:** ¿qué diferencia hay entre `Vec` y `GF2`, y por qué el código no las junta en una sola clase?

## Field vs vector space

- **Field** (`GF2.py`) = el conjunto de *valores escalares* y sus reglas de aritmética (+, ×, −, /). R, C y GF(2) son 3 fields distintos que el libro usa. GF(2) solo tiene 2 elementos (`0`, `one`), suma = XOR: `one+one=0`.
- **Vec** (`vec.py`) = estructura de vector, genérica sobre CUALQUIER field. No sabe nada de aritmética — solo domain `D` + dict `f`. Sus operaciones (`add`, `dot`, `scalar_mul`) delegan la aritmética real (`+`, `*`) al objeto que esté guardado como valor.

## Por qué separados

1. **Reuse sin herencia** — mismo `Vec` sirve para `R^n`, `C^n`, `GF(2)^n` sin tocar `vec.py`. Cambiás qué objetos metés en el dict (`float`, `complex`, `one`) y `Vec` funciona igual — duck typing vía `__add__`/`__mul__` de cada valor, no polimorfismo por herencia.
2. **Confirmado en el libro** (Cap 5, Problem 5.14.14, p.324): "you should use the value `one` defined in the module `GF2` in place of the number 1" — mismo `Vec`, mismo código, solo cambia qué field usás para los valores.
3. **Estructura del libro:** Cap 1 = "The Field" (abstrayendo R/C/GF(2), sección 1.3 "Abstracting over fields") viene ANTES de Cap 2 = "The Vector" — el vector space se define matemáticamente *sobre* un field arbitrario, el código sigue la misma separación.

## Conexión con Axler

Vector space = (set de vectores, field, +, ·) — Axler también generaliza sobre field $\mathbf{F}$. Klein lo hace literal en código: `Vec` = vector space genérico, `GF2` = una instancia concreta de field, intercambiable con `float`/`complex` sin cambiar `Vec`.

## Fuente

Verificado leyendo directo el PDF local (pdftotext), TOC Cap 1-2 y texto del Problem 5.14.14 — no memoria, no web (libro completo ya en el vault).
