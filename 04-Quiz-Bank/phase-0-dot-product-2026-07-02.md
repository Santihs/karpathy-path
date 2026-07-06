---
tags: [phase-0, linear-algebra, dot-product, coding-the-matrix, klein]
date_added: 2026-07-02
last_tested: null
---

Q: ¿Qué es el dot-product de dos D-vectores u, v, y qué tipo de valor devuelve?
A: $\mathbf{u}\cdot\mathbf{v} = \sum_{k\in D} u[k]\,v[k]$ — suma de productos de entradas correspondientes. Devuelve un ESCALAR, no un vector (por eso también se llama "scalar product").

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: ¿Cómo se implementa list_dot(u,v) en Python con sum() + list comprehension?
A: `def list_dot(u, v): return sum([u[i]*v[i] for i in range(len(u))])` — o equivalente con zip: `sum([a*b for (a,b) in zip(u,v)])`.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: Tenés cost=[precio por unidad] y quantity=[cantidad de cada item]. ¿Qué operación te da el costo total, y por qué?
A: cost·quantity (dot-product) — suma cada precio×cantidad. Patrón general "suma ponderada", mismo patrón que weights·features en regresión lineal / capa densa.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: Needle-in-haystack matching con vectores ±1: ¿qué significa que el dot-product en una posición dé el valor máximo posible (=len(needle))?
A: Match perfecto — cada entrada del needle coincide en signo con la porción correspondiente del haystack en esa posición. Base conceptual de cross-correlation/convolution en CNNs.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: haystack=[1,-1,1,1,1,-1,1,1,1], needle=[1,-1,1,1,-1,1]. ¿Cuántas posiciones de inicio son posibles, y cuál es el resultado de los dot-products?
A: 9-6+1=4 posiciones (0,1,2,3). Resultados: [2,2,0,0] — mejor match empatado en posición 0 y 1.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: Dot-product sobre GF(2): ¿qué representa u·v cuando u es el vector all-ones [1,1,1,...,1]?
A: La PARIDAD de v — 1 si v tiene cantidad impar de 1s, 0 si tiene cantidad par. Dot-product con all-ones = sumar todas las entradas de v sin pesar nada, y en GF(2) esa suma total ES la paridad.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: ¿Por qué el dot-product con all-ones sobre GF(2) es la base de un parity bit / checksum?
A: Porque detecta si la cantidad de 1s cambió de paridad — si un bit se corrompe en transmisión, la paridad calculada ya no coincide con la esperada, señal de error. Base de ECC memory, RAID, checksums de red.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: (repaso 2026-07-03) cost·quantity = costo total. ¿Qué patrón general de ML reaparece acá, y en qué contexto?
A: "Suma ponderada" — mismo patrón que weights·features en regresión lineal o capa densa de una red neuronal. Dot-product en general = combinar valores con pesos y sumar.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: (repaso 2026-07-03) haystack=[1,-1,1,1,1,-1,1,1,1] (len 9), needle=[1,-1,1,1,-1,1] (len 6). Sin mirar la nota: ¿cuántas posiciones de inicio hay, y cuánto da el dot-product en pos 0?
A: Posiciones = 9-6+1 = 4 (0,1,2,3). Pos 0: [1,-1,1,1,1,-1]·needle = 1+1+1+1-1-1 = 2. Resultado completo: [2,2,0,0].

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: (repaso 2026-07-03) GF(2), u·v con u=all-ones. El resultado es 0 o 1 — ¿pero qué SIGNIFICA ese valor?
A: No es solo "0 o 1" trivial de GF(2) — significa la PARIDAD de v (par/impar cantidad de 1s). Ese significado es lo que lo hace útil como parity bit/checksum: detecta cambio de paridad = bit corrupto.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: (2026-07-03) Enunciá las 3 propiedades algebraicas del dot-product (Prop. 2.9.21/2.9.22/2.9.25) y de dónde sale cada una.
A: Commutativity `u·v = v·u` (se hereda de que la multiplicación escalar-escalar es conmutativa). Homogeneity `(αu)·v = α(u·v)` (escalar un lado del dot-product equivale a escalar el resultado). Distributivity `(u+v)·w = u·w + v·w` (se prueba expandiendo entrada por entrada).

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: (2026-07-03) ¿Por qué `(αu)·(αv) ≠ α(u·v)` en general (Problem 2.9.24)?
A: El escalar se aplica a AMBOS lados del dot-product, así que se duplica: `(αu)·(αv) = α²(u·v)`, no `α(u·v)`. Homogeneity solo garantiza escalar UN lado a la vez.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: (2026-07-03) En la implementación `Vec.dot(u,v)`, ¿por qué hace falta `assert u.D == v.D` antes de sumar, en vez de solo iterar `zip(u.f, v.f)`?
A: `u.f`/`v.f` son dicts sparse — pueden tener distintas claves presentes (ausente = 0 implícito). `zip` sobre los dicts sparse desalinearía o saltearía entradas. Hay que iterar sobre el domain declarado `D`, no sobre el storage sparse.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: (2026-07-03) `equal()` en `Vec` compara con `==` exacto, entrada por entrada. ¿Qué debilidad tiene esto con floats, y por qué NO se arregla poniendo tolerancia dentro de `equal()`?
A: `0.1+0.2 != 0.3` exacto en floats (error de redondeo acumulado) — vectores matemáticamente iguales comparan distintos. No se arregla con tolerancia dentro de `equal()` porque esa misma función debe seguir siendo EXACTA para fields como GF(2)/int, donde tolerancia rompería la corrección. La solución (Klein) es un helper separado (`is_almost_zero`) aplicado en el call site, no dentro de `__eq__`.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: (2026-07-03) En `triangular_solve_n`, la línea `x[i] = (b[i] - rowlist[i] * x) / rowlist[i][i]` usa dot-product. ¿Cómo hace el dot-product para "ignorar" las variables todavía no resueltas?
A: `x` arranca en el vector cero y se llena de atrás para adelante. Las posiciones todavía no resueltas valen 0 en `x`, así que en el dot-product `coef * 0 = 0` — no aportan nada a la suma automáticamente, sin lógica especial.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: (2026-07-03) Si `rowlist[i][i] == 0` en un sistema triangular, ¿qué implica matemáticamente (Prop. 2.11.6), y qué se hace en la práctica cuando la matriz general (no triangular) tiene ese problema?
A: Implica que existe al menos un `b` para el cual el sistema NO tiene solución — no es solo un límite del código. En la práctica (matriz no triangular pero invertible) se usa *partial pivoting*: reordenar filas para mover un valor no-cero a la diagonal — es la `P` en `A=PLU` que usa LAPACK `getrf` (la rutina detrás de `torch.linalg.solve`). Si ningún reordenamiento alcanza, la matriz es singular de verdad — ahí ya no aplica triangular solve.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->
