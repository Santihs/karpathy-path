---
tags: [phase-0, linear-algebra, dot-product, duality, cross-product]
date_added: 2026-06-29
last_tested: 2026-07-07
---

Q: ¿Qué tipo de resultado produce el producto punto? ¿Y el producto cruz?
A: Producto punto → escalar (un número). Producto cruz → vector (perpendicular a los dos de entrada). Esta diferencia es fundamental.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: ¿Qué significa geométricamente que v·w = 0?
A: Los vectores son perpendiculares (ortogonales) — no comparten ninguna dirección. Ángulo entre ellos = 90°.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: Dado v = [2, 0] y w = [1, 1], ¿cuánto de w va en la dirección de v?
A: comp = (v·w) / |v| = (2×1 + 0×1) / 2 = 1. La "sombra" de w sobre v tiene longitud 1.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: ¿Por qué en attention de transformers se usan productos punto?
A: Cada producto punto Q·Kᵀ mide cuánto "apunta" una query en la dirección de una key — es similitud direccional. Alto producto punto = alta relevancia.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: Explica dualidad en una oración.
A: Cualquier transformación lineal nD→1D puede escribirse como producto punto con un vector en nD — proyectar y transformar son la misma operación.

<!-- srs: ease=2.5 interval=1 due=2026-07-08 lapses=0 last_seen=2026-07-07 -->

---

Q: Si û = [0.8, 0.6] y lo uso como transformación 2D→1D, ¿dónde aterrizan î y ĵ?
A: î aterriza en 0.8 (coordenada x de û), ĵ aterriza en 0.6 (coordenada y de û). Las coordenadas de û son exactamente los landing points.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: ¿Para qué dimensiones está definido el producto cruz?
A: Solo en 3D (y matemáticamente en 7D, pero ignorar). El producto punto funciona en cualquier dimensión.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: ¿Qué representa geométricamente |v × w|?
A: El área del paralelogramo formado por v y w. Igual que |v||w|sin(θ).

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: Conexión entre producto cruz y dualidad: ¿cómo se deriva v × w usando dualidad?
A: Define f(p) = det([p, v, w]) — función lineal 3D→1D. Por dualidad, existe un vector dual q tal que f(p) = q·p. Ese vector q es exactamente v×w. El producto cruz es el dual de la función volumen.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: Una red neuronal tiene embeddings de 512 dimensiones. ¿Cómo uses dot product para medir similitud entre dos embeddings?
A: Normaliza ambos (hazlos unitarios), luego dot product = cos(θ). Resultado cercano a 1 = similares. Cercano a 0 = independientes. Cercano a -1 = opuestos. Cosine similarity = (v·w) / (|v| × |w|).

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: Explica paso a paso cómo dualidad deriva la fórmula del cross product (no solo "nD→1D").
A: 1) Defines f(x) = det([x,v,w]) — lineal en x, da un escalar. 2) Dualidad: existe p fijo tal que f(x) = p·x para todo x. 3) Expandes el determinante en componentes y comparas coeficientes con p₁x+p₂y+p₃z. 4) Resuelves p → p = v×w.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: ¿Por qué el "determinante" con î, ĵ, k̂ en la primera fila NO es un determinante real? ¿Y qué relación tiene con el área del paralelogramo?
A: Un determinante real solo tiene escalares como entradas — ahí hay vectores, rompe la definición. Es mnemotécnico: incluye 3 cofactores que resultan en un vector, no en un escalar de escala. La relación con área es aparte: |v×w| (norma del vector resultado) = área del paralelogramo — eso no es lo que "calcula" el mnemotécnico directamente, es un hecho geométrico sobre el resultado.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: ¿Cuál es la diferencia entre "determinante real" (ch6) y el mnemotécnico usado para cross product (ch10)?
A: Determinante real = número, factor de escala de área/volumen de una transformación. Mnemotécnico de cross product = truco con misma estructura de cofactores pero entradas vectoriales (î,ĵ,k̂) → resultado es un vector (v×w), no una escala. Comparten nombre y estructura de cálculo, pero son operaciones distintas.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->
