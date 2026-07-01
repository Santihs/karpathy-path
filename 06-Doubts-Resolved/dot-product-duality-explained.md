---
tags: [phase-0, linear-algebra, dot-product, duality]
date_resolved: 2026-06-30
---

# Producto punto y dualidad — explicación verificada

## Pregunta
Explicar producto punto (dot product) basado en 3Blue1Brown "Essence of Linear Algebra" ch 9, con diagrama.

## Respuesta

**Dos fórmulas, mismo resultado:**
- Geométrica: `v·w = |v||w|cos(θ)`
- Por componentes: `v·w = v1w1 + v2w2`

**Por qué coinciden (dualidad):** toda transformación lineal de un espacio n-dimensional a los números reales (2D→1D en el caso simple) puede representarse como una matriz 1×n. Aplicar esa matriz a un vector x resulta ser geométricamente idéntico a proyectar x sobre un vector fijo w y escalar por su longitud — "tiplear" w de vector-columna a matriz-fila (transponer) da exactamente esa transformación. Por eso:

> "el dual de un vector es la transformación lineal que codifica, y viceversa" — cada vector w define una función `f(x) = w·x`, y cada función lineal escalar tiene un único vector w que la representa.

Esto explica por qué la fórmula mecánica (sumar productos de componentes) y la fórmula geométrica (proyección × longitud) son la misma operación vista desde dos ángulos.

**Caso especial:** vectores perpendiculares → proyección = 0 → dot product = 0. Signo del dot indica si apuntan en direcciones similares (+) u opuestas (-).

**Conexión a ML:** cada neurona computa `y = w·x + b`. El vector de pesos w es literalmente el "dual" — la función lineal que mide cuánto se alinea el input x con la dirección que la neurona busca. Ver [[duality-in-neural-networks]].

Diagrama: [dot-product-duality.excalidraw](../02-Topics/diagrams/dot-product-duality.excalidraw)

## Fuentes
- [Dot products and duality | Chapter 9, Essence of linear algebra — 3Blue1Brown (YouTube)](https://www.youtube.com/watch?v=LyGKycYT2v0)
- [Dot Products and Duality — Notes by Lex Toumbourou](https://notesbylex.com/dot-products-and-duality)
