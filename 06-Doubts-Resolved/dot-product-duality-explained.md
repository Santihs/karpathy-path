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

## Repaso 2026-07-22 (4to intento — rewatch completo del capítulo)

Tercera falla registrada en quiz (06-30, 07-03, 07-07) — esta vez rewatch completo en vez de solo repregunta. Lo que hizo clic fue la secuencia de imágenes del video en orden:

1. "Where do î and ĵ land?" — proyectar los vectores base sobre la recta de û da directamente las 2 entradas de la matriz 1×2.
2. Equivalencia final: `[ux uy][x,y] = ux·x + uy·y = [ux,uy]·[x,y]` — multiplicar por la matriz fila y hacer dot-product con el vector columna [ux,uy] son la MISMA cuenta, número por número.

Confirmación propia en la sesión: "es una transformation entonces igual el producto punto?" — correcto. Cualquier transformación lineal nD→1D = dot-product con el vector dual (la matriz fila leída como vector columna).

Necesita para no ser el 5to fallo: usar û unitario específicamente (no vector cualquiera) es lo que hace que la proyección de î/ĵ dé la matriz sin factor de escala extra — ver [[vector-unitario-normalizacion]].

## Repaso 2026-08-07 — proyección escalar con v NO unitario, ¿de dónde sale la división?

Pregunta puntual sobre carta Anki: `comp = (v·w)/|v|` — ¿por qué dividir por |v|?

**Derivación:** parto de la fórmula geométrica `v·w = |v||w|cos(θ)`. La sombra (proyección escalar) de w sobre la dirección de v es, por definición, `|w|cos(θ)` — la parte de w que "apunta como" v, medida en unidades de longitud, sin el factor |v| metido.

Despejando `|w|cos(θ)` de la fórmula geométrica:
```
v·w = |v| · (|w|cos(θ))
|w|cos(θ) = (v·w) / |v|
```

La división cancela el |v| que el dot product mete de más. Sin dividir, `v·w` mezcla dos cosas: la sombra real y el tamaño de v (si v fuera el doble de largo, v·w se duplica aunque la sombra de w no cambió). Dividir por |v| es lo mismo que primero normalizar v a v̂=v/|v| y hacer `v̂·w` — conecta directo con la nota de arriba sobre "usar û unitario" para que el dot dé la proyección limpia.

**Chequeo numérico** (v=[2,0], w=[1,1]): `v·w = 2·1+0·1 = 2`, `|v|=2`, `comp = 2/2 = 1`. Verificación geométrica directa: v apunta en eje x puro, entonces la sombra de w sobre esa dirección es simplemente la componente x de w, que es 1. Coincide.

Fuente verificada: [Scalar projection — Wikipedia](https://en.wikipedia.org/wiki/Scalar_projection) confirma `comp_v(w) = (v·w)/|v|` como fórmula estándar de proyección escalar (a veces con valor absoluto de |v| si se quiere magnitud sin signo, pero la versión con signo es la estándar en este contexto de duality).
