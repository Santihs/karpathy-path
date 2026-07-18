---
tags: [phase-0, math, linear-algebra, coding-the-matrix, basis, span, compression]
status: learning
first_learned: 2026-07-17
last_reviewed: 2026-07-17
confidence: 3/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Coding the Matrix — Cap 5: The Basis (Klein)

Nota: el roadmap sigue **Klein**, no Axler — Axler quedó pausado por exceso de jerga matemática pura, Klein encaja mejor con perfil de software developer.

---

## 1. Coordinate systems (5.1)

### 5.1.1 — La idea de Descartes

Descartes (1618) notó que la posición de un punto (la mosca en el techo) se puede describir con 2 números: distancia a 2 paredes de referencia — **incluso si las paredes no son perpendiculares**. Reduce geometría a álgebra.

### 5.1.2 — Representación de coordenadas

Un sistema de coordenadas para un espacio vectorial `V` se especifica con generadores `a1,...,an`. Todo vector `v` en `V` se escribe como combinación lineal:

```
v = α1*a1 + α2*a2 + ... + αn*an
```

Los pesos `[α1,...,αn]` son la **representación de coordenadas** de `v`. Analogía: los generadores son ingredientes fijos, las coordenadas son "cuánto de cada ingrediente" para reconstruir `v`. Multiplicar por `αi` = amplificar (estirar/encoger, o dar vuelta si es negativo) el generador `ai` antes de sumarlos.

Para que esto funcione sin ambigüedad, cada vector debe tener representación **única** en esos generadores (existencia/unicidad — Klein lo trata en 5.7.1, todavía no visto).

**Example 5.1.1:** `v=[1,3,5,3] = 1*[1,1,0,0] + 2*[0,1,1,0] + 3*[0,0,1,1]` → coordenadas `[1,2,3]`.

**Example 5.1.2** (verificado componente a componente): coordenadas de `[6,3,2,5]` en términos de `[2,2,2,3], [1,0,-1,0], [0,1,0,1]`:

| posición | 2·a1 | 2·a2 | -1·a3 | suma | v esperado |
|---|---|---|---|---|---|
| 1 | 4 | 2 | 0 | 6 | 6 ✓ |
| 2 | 4 | 0 | -1 | 3 | 3 ✓ |
| 3 | 4 | -2 | 0 | 2 | 2 ✓ |
| 4 | 6 | 0 | -1 | 5 | 5 ✓ |

→ coordenadas `[2, 2, -1]`.

**Example 5.1.3** (mismo patrón sobre GF(2)): coordenadas de `[0,0,0,1]` en `[1,1,0,1],[0,1,0,1],[1,1,0,0]` → `[1,0,1]`.

### 5.1.3 — Coordenadas y matrix-vector multiplication

Conecta directo con Cap 4 (matrix-vector mult). Armás la matriz `A` con los generadores como **columnas**: `A = [a1 | a2 | ... | an]`.

"`u` es la representación de coordenadas de `v` en `a1,...,an`" se escribe como:

```
A * u = v
```

- **coordenadas → vector**: multiplicás `A*u`, directo.
- **vector → coordenadas**: hay que **resolver** `A*x = v` (sistema de ecuaciones) — mismo tipo de problema que `find_triangular_order`/`triangular_solve` de Cap 4.6.4, pero acá `A` no tiene por qué ser triangular.

Verificado con Example 5.1.2 tratado como `A*u=v` (misma tabla de arriba, ahora leída como producto punto fila-por-fila de `A` con `u`).

---

## 2. First look at lossy compression (5.2)

Problema: guardar muchas imágenes 2000×1000 grayscale (`D`-vector) de forma compacta. Klein prueba 3 estrategias.

### Strategy 1 — podar valores por magnitud (5.2.1)

Reemplazar el vector por el **k-sparse** más cercano (solo `k` entradas no-cero): quedarte con las `k` entradas de mayor magnitud, resto en cero. ("Closest" formalmente se define recién en Cap 8, distancia).

**Example 5.2.2:** imagen `[200,75,200,75]`, 2-sparse más cercano = `[200,0,200,0]` (se conservan las dos entradas de magnitud 200). Suprimir el 90% de una foto real así deja manchas — pierde mucho.

**¿Se puede escribir como multiplicación matriz-vector?** Sí, para un `v` fijo: `D*v` con `D` matriz diagonal de 0s/1s marcando qué posiciones conservar. Pero `D` depende de los *valores* de `v` (qué posiciones tienen mayor magnitud) — no hay una `D` fija que sirva para cualquier vector. La operación "top-k sparsify" en general **no es una transformación lineal fija**, es data-dependent: primero mirás `v` para decidir `D`, después multiplicás.

### Strategy 2 — guardar coordenadas, sin pérdida (5.2.2)

Elegir generadores `a1,...,an` de antemano, guardar solo `u` (coordenadas) en vez de la imagen entera. Recuperar con `A*u`.

**Example 5.2.3:** `a1=[255,0,255,0]`, `a2=[0,255,0,255]`. `[200,75,200,75] = (200/255)*a1 + (75/255)*a2` → coordenadas `[200/255, 75/255]` (2 números en vez de 4 — compresión sin pérdida).

**Falla:** `[255,200,150,90]` no se puede representar — no está en `span{a1,a2}`. Ver [[span-de-vectores]].

**Fundamental Questions que abre esto:**
- 5.2.4 — dado `V`, ¿cómo saber si `V = span{a1,...,an}`?
- 5.2.5 — ¿cuál es el mínimo de vectores cuyo span = `V`?

Spoiler de Klein: Strategy 2 termina fallando porque garantizar que CUALQUIER imagen sea representable exige que el span cubra `R^D` entero, y el mínimo `n` para eso resulta tan grande que no hay compresión real.

### Strategy 3 — híbrida (la que funciona)

Combina las 2 anteriores: podar, pero en el espacio de **coordenadas**, no en píxeles crudos.

```
1. Elegir generadores a1,...,an
2. Para cada imagen v, hallar coordenadas u  (resolver A*x=v)
3. Podar u → guardar el k-sparse más cercano ũ
4. Para recuperar: A*ũ
```

2 condiciones necesarias:
- **Paso 2 siempre debe funcionar** → `span{a1,...,an}` = espacio completo.
- **Paso 3 no debe distorsionar mucho** → la info debe quedar concentrada en pocas coordenadas grandes, para que podar el resto no se note.

Con buenos generadores (Cap 10 — tipo Fourier/wavelet), Klein logra buena imagen guardando solo 10% de los números.

**Conexión con ML real:** esto es exactamente el patrón detrás de JPEG (DCT + poda de coeficientes chicos) y de magnitude pruning en redes neuronales (podar pesos de menor magnitud). Ver [[compresion-basis-jpeg-pruning-ml]].

---

## Doubts Resolved
- [[span-de-vectores]] — qué es el span de un conjunto de vectores, por qué algunas imágenes quedan fuera.
- [[compresion-basis-jpeg-pruning-ml]] — cómo esta idea de Klein es literalmente JPEG y magnitude pruning en ML.

## Próximo
Klein Cap 5, sección 5.3+ — Fundamental Questions 5.2.4/5.2.5 (span test, basis, dimensión).
