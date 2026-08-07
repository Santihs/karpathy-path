---
tags: [phase-0, math, linear-algebra, coding-the-matrix, gaussian-elimination, echelon-form, null-space, rank, gf2, rsa, factoring]
status: learning
first_learned: 2026-08-07
last_reviewed: 2026-08-07
confidence: 4/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Coding the Matrix — Cap 7: Gaussian Elimination (Klein)

Nota: el roadmap sigue Klein, no Axler (ver [[Coding-the-Matrix-Basis]]). Este capítulo cierra: base del row space, resolver Ax=b, base del null space, y dos labs (secret-sharing + factoring de enteros vía quadratic sieve).

## 7.0 — Objetivo del capítulo

Gaussian elimination sirve para 4 problemas relacionados:
- Encontrar base del span de vectores dados (da el rank)
- Testear independencia lineal de un conjunto de vectores
- Encontrar base del null space de una matriz
- Resolver una ecuación matriz-vector (= expresar un vector como combinación lineal de otros = resolver un sistema lineal)

## 7.1 — Echelon form

**Definición 7.1.1:** matriz m×n está en echelon form si, para cualquier fila, si su primera entrada no-cero está en posición k, toda fila anterior tiene su primera entrada no-cero en una posición < k. Forma "escalera" descendente. Caso especial: matriz triangular. Si una fila es toda cero, todas las siguientes también deben serlo.

**Lemma 7.1.2:** si una matriz está en echelon form, las filas no-cero forman una base del row space.

### De naive a correcto (7.1.2-7.1.4)

Primer intento (ordenar filas por posición del primer no-cero) falla: si ninguna fila restante tiene no-cero en la columna actual, `list index out of range`. Arreglar solo el crash no alcanza — el resultado puede seguir violando la definición de echelon form.

**Solución real:** *elementary row-addition operations* — cuando se selecciona la fila pivot para una columna, hay que restar múltiplos de esa fila a TODAS las demás filas que tengan no-cero en esa columna, para hacerlas cero ahí. El bug original era de diseño incompleto (faltaba este loop), no un edge case a parchear.

**Por qué cambian los valores de una fila:** se reemplaza la fila por sí misma menos un múltiplo de la fila pivot. Ejemplo real (ejemplo ℝ del capítulo): `row3=[0,0,0,6,7]`, pivot=`row1=[0,0,0,3,2]`, multiplier=6/3=2 → `row3_nuevo = row3 - 2*row1 = [0,0,0,0,3]` (el 7 también cambia porque se resta el vector ENTERO). Es reversible — sumando de vuelta `2*row1` se recupera el original — por eso no se pierde información, solo cambia la representación.

**Por qué hay que "eliminar" (llevar a cero) en vez de parar antes:** hasta procesar TODAS las columnas no se puede saber si una fila es redundante o si "le queda info escondida" en una columna no procesada. Ejemplo: la fila 5 del ejemplo ℝ parecía tener contenido (`[0,0,0,0,2]`) después de la columna 3 — recién al procesar la columna 4 se reveló que era combinación lineal de las demás. Cortar antes de tiempo da rank/independencia mal calculados (falso positivo).

### 7.1.5-7.1.6 — Por qué el algoritmo es correcto

Restar un múltiplo de una fila de otra = multiplicar la matriz por una *elementary row-addition matrix* (identidad con un elemento off-diagonal), que es invertible.

**Lemma 7.1.3:** Row(NA) ⊆ Row(A) para cualquier N. **Corollary 7.1.4:** si M es invertible, Row(MA) = Row(A) — se prueba con ambas inclusiones (una directa con N=M, la otra con N=M⁻¹ sobre B=MA, usando M⁻¹(MA)=(M⁻¹M)A=A). Esta es la invariante central del capítulo: multiplicar por una matriz invertible (como el producto de row-addition operations) nunca cambia el row space, solo la forma.

### 7.1.8-7.1.9 — Cuándo falla, y pivoting

Con floating-point, la aritmética inexacta puede dar rank mal calculado. Ejemplo: matriz con 10⁻²⁰ y 10²⁰ — al restar `10²⁰ × fila1` de fila2, Python computa `1 - 1e20 = -1e20` (el 1 se "swampea", perdido por la magnitud tan distinta). **Pivoting** (partial: elegir la fila con mayor valor absoluto en la columna como pivot; complete: elegir también la columna dinámicamente) evita estos desastres — partial es lo más usado en la práctica.

## 7.2 — Gaussian elimination sobre GF(2)

Sobre GF(2) toda la aritmética es exacta (no hay floating-point) — misma lógica columna por columna, pero sin errores de precisión porque `-1=1`. Ver visualizador para el ejemplo trabajado.

## 7.3 — Existe M invertible tal que MA está en echelon form

Cada row-addition operation = multiplicar por una matriz M_i. Encadenando todas da M̄A; reordenando filas de M̄ (para que queden en orden correcto de pivot) se obtiene M. Es invertible porque es producto de invertibles + reordenamiento de filas linealmente independientes (Proposition 7.3.1).

**Computar M sin multiplicar matrices (7.3.2):** se mantienen dos row-lists en paralelo — `rowlist` (transformándose) y `M_rowlist` (transformadora, inicializada como identidad), con invariante `M_rowlist·(matriz inicial) = rowlist`. Cada row-addition operation sobre `rowlist` se aplica IGUAL sobre `M_rowlist`. Es el equivalente en software a un **log de migraciones / event log**: en vez de recalcular el estado final desde cero, grabás cada cambio — podés re-aplicarlo, auditarlo, revertirlo.

## 7.4 — Resolver Ax=b usando Gaussian elimination

Computar M tal que MA=U en echelon form, multiplicar ambos lados: Ux=Mb. Como M es invertible, x resuelve la original SSI resuelve la nueva (más fácil, porque U es echelon).

- **Caso invertible:** backward substitution (Cap 2.11, ya visto — ver `05-Projects/coding-the-matrix/src/coding_the_matrix/triangular.py`).
- **Filas cero:** se ignoran; si el b correspondiente no es cero, no hay solución (el algoritmo no lo detecta automáticamente).
- **Columnas irrelevantes** (ninguna fila tiene su primer no-cero ahí): se descartan, se resuelve el sistema reducido, y a esas variables se les asigna 0 (no aportan nada a la combinación lineal).
- **Atacando el esquema de autenticación simple (7.4.4):** Eve arma Ax=b con los pares espiados; cuando rank(A)=n, Gaussian elimination rompe el password. Contramedida: introducir errores random — Gaussian elimination NO funciona con b's corruptos, y no se conoce algoritmo eficiente para resolver con errores sobre GF(2) (problema computacionalmente difícil).

## 7.5 — Base del null space

Dada A, se busca base de {v : v·A = 0} (null space de A^T). Se computa M tal que MA=U en echelon form. Para cada fila u_i de U que es vector cero, la fila correspondiente b_i de M cumple b_i·A=0.

**Prueba de que son base:** linealmente independientes (subconjunto de filas de M, que es invertible). Generan el espacio completo vía Rank-Nullity Theorem: m = rank(A) + nullity(A^T), y el número de filas cero de U es exactamente s = nullity(A^T).

**Ejercicio resuelto (Problem 7.9.9):** dada A y M del libro, se pide listar filas u de M tales que u·A=0. Solo la fila 4 de MA es vector cero → fila 4 de M `(0,0,one,0,one)` es la base (1 vector). Verificación a mano: las filas c y e de A son idénticas → c+e=0 en GF(2), confirma la dependencia detectada.

## 7.6-7.8 — Factoring integers (RSA, quadratic sieve)

**Teorema fundamental:** todo N>1 tiene única bolsa de primos cuyo producto es N. Factorizar es difícil (a diferencia de testear primalidad) — RSA depende de eso.

**Trial division:** N-2 divisiones ingenuo; mejora a √N divisiones (todo compuesto tiene divisor no-trivial ≤√N); mejora extra probando solo primos ≤√N (Prime Number Theorem). Aun así, RSA con ~10 dígitos más de margen hace esto inviable (factor ~10,000x más lento, cifra aproximada del propio Klein — el escalado real de trial division es √N, así que 10 dígitos más de N implica más cerca de ~100,000x).

**Quadratic sieve (7.8.4-7.8.10):** en vez de a²-b²=N exacto (difícil), se busca a²-b² DIVISIBLE por N. Se generan candidatos x tales que x²-N factoriza completamente sobre un `primeset` chico — cada factorización se codifica como vector GF(2) (`make_Vec`, paridad de exponentes vía `int2GF2`). Con K+1 vectores en un espacio de dimensión K, son necesariamente dependientes (Dimension Principle) — Gaussian elimination encuentra la combinación que suma cero, lo que da un producto que es cuadrado perfecto: `(x1²-N)(x2²-N)... = b²`. Entonces `a²-b² = kN` con `a` = producto de los x_i, y `gcd(a-b, N)` da (con suerte) un divisor no-trivial. Si rank(rowlist) < len(rowlist), hay MÚLTIPLES combinaciones posibles para reintentar si la primera falla.

**Threshold secret-sharing (7.7):** compartir un secreto entre 4 TAs de forma que cualquier 3 lo recuperen pero 2 no. Con vectores 6D en pares (a_i,b_i) donde cualquier 3 pares son linealmente independientes: 3 TAs arman sistema 6×6 invertible → recuperan secreto (Recoverability). 2 TAs tienen sistema incompleto (4 ecs, 6 incógnitas) → consistente con cualquier valor del secreto → cero info filtrada (Secrecy). Es la misma idea detrás de Shamir's Secret Sharing (HashiCorp Vault, AWS KMS): k de n partes necesarias, k-1 partes no filtran nada.

## Implementación propia

`05-Projects/coding-the-matrix/src/coding_the_matrix/echelon.py` — motor único `_gaussian_elimination`, 4 fachadas públicas: `transformation`, `echelon_form`, `row_reduce`, `null_space_basis`. 10 tests en `tests/test_echelon.py`, 120 tests totales del proyecto pasan.

Decisiones de diseño:
- **No mutar la lista de entrada** — copia local antes de operar.
- **`key=repr` en vez de `key=hash`** para ordenar columnas — el hash de strings se randomiza por proceso en Python 3 (seguridad), rompería reproducibilidad de tests. `repr` es igual de arbitrario pero estable.
- **M como "log de migraciones"** — se aplican las mismas row-addition operations en paralelo sobre `M_rowlist` (identidad inicial) en vez de recalcular MA por fuerza bruta.

## Visualizador interactivo

`05-Projects/coding-the-matrix/src/coding_the_matrix/visualize_gaussian.py` — matplotlib interactivo (preferido sobre gif: permite pausar y pensar cada paso, no autoplay). `_gaussian_elimination` se instrumentó con parámetro opcional `record` sin tocar su interfaz pública.

Correr: `cd 05-Projects/coding-the-matrix && uv run python -m coding_the_matrix.visualize_gaussian`

Controles: ←/→ o A/D avanza/retrocede, E cambia entre ejemplo ℝ (5×5, Sec 7.3.2, 8 frames) y GF(2) (4×4, Sec 7.2, 7 frames), Q cierra. Resalta fila pivot (verde) y fila modificándose (naranja).

**Ojo:** los snapshots muestran el array de trabajo en el orden ORIGINAL de filas, no el `new_rowlist` reordenado por columna de pivot — para leer la escalera real hay que reordenar mentalmente por orden de pivot. Ejemplo GF(2) al step final: pivots A→row1, B→row3, C→row0, D→row2; ninguna fila cero → rank=4=todas las filas → matriz invertible, full rank (contraste con ejemplo ℝ donde la fila 5 sí da cero → rank 4 de 5).

Dependencia agregada: `matplotlib>=3.9.0` en `pyproject.toml`.

## Por qué importa para ML/AI

Resolver sistemas lineales y encontrar rank/dependencias es la base de mínimos cuadrados, PCA, y cualquier fit de modelo lineal. El patrón "instrumentar el algoritmo con un callback opcional sin tocar su interfaz pública" (usado para el visualizador) es una técnica general útil para debugging/observability de cualquier pipeline de entrenamiento.
