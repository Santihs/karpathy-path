---
tags: [phase-0, linear-algebra, dot-product, coding-the-matrix, klein]
date_added: 2026-07-02
last_tested: null
---

Q: ¿Qué es el dot-product de dos D-vectores u, v, y qué tipo de valor devuelve?
A: $\mathbf{u}\cdot\mathbf{v} = \sum_{k\in D} u[k]\,v[k]$ — suma de productos de entradas correspondientes. Devuelve un ESCALAR, no un vector (por eso también se llama "scalar product").

---

Q: ¿Cómo se implementa list_dot(u,v) en Python con sum() + list comprehension?
A: `def list_dot(u, v): return sum([u[i]*v[i] for i in range(len(u))])` — o equivalente con zip: `sum([a*b for (a,b) in zip(u,v)])`.

---

Q: Tenés cost=[precio por unidad] y quantity=[cantidad de cada item]. ¿Qué operación te da el costo total, y por qué?
A: cost·quantity (dot-product) — suma cada precio×cantidad. Patrón general "suma ponderada", mismo patrón que weights·features en regresión lineal / capa densa.

---

Q: Needle-in-haystack matching con vectores ±1: ¿qué significa que el dot-product en una posición dé el valor máximo posible (=len(needle))?
A: Match perfecto — cada entrada del needle coincide en signo con la porción correspondiente del haystack en esa posición. Base conceptual de cross-correlation/convolution en CNNs.

---

Q: haystack=[1,-1,1,1,1,-1,1,1,1], needle=[1,-1,1,1,-1,1]. ¿Cuántas posiciones de inicio son posibles, y cuál es el resultado de los dot-products?
A: 9-6+1=4 posiciones (0,1,2,3). Resultados: [2,2,0,0] — mejor match empatado en posición 0 y 1.

---

Q: Dot-product sobre GF(2): ¿qué representa u·v cuando u es el vector all-ones [1,1,1,...,1]?
A: La PARIDAD de v — 1 si v tiene cantidad impar de 1s, 0 si tiene cantidad par. Dot-product con all-ones = sumar todas las entradas de v sin pesar nada, y en GF(2) esa suma total ES la paridad.

---

Q: ¿Por qué el dot-product con all-ones sobre GF(2) es la base de un parity bit / checksum?
A: Porque detecta si la cantidad de 1s cambió de paridad — si un bit se corrompe en transmisión, la paridad calculada ya no coincide con la esperada, señal de error. Base de ECC memory, RAID, checksums de red.
