---
tags: [phase-0, math, linear-algebra, coding-the-matrix, orthogonalization, gram-schmidt, projection, least-squares, qr-factorization, basis]
status: solid
first_learned: 2026-08-09
last_reviewed: 2026-08-10
confidence: 4/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Coding the Matrix — Cap 9: Orthogonalization (Klein)

Nota: sigue de [[Coding-the-Matrix-Inner-Product]]. Sesión densa, marcada como `learning` (no `solid`) — pendiente repaso antes de seguir con 9.4 en adelante.

## 9.0 — El problema general

Cap 8 resolvió: punto más cercano a `b` en la línea generada por **1** vector `v` (fire engine problem). Cap 9 generaliza a **n** vectores:

**Computational Problem 9.0.4:** dado `b` y `v1,...,vn`, encontrar el vector en `Span{v1,...,vn}` más cercano a `b`.

**Conexión con least-squares:** con `A = [v1|...|vm]` (matriz por columnas), `Span{v1,...,vm} = {Ax : x}`. Encontrar los coeficientes de la combinación = encontrar `x` que minimiza `||b - Ax||` — el problema de **least-squares**. Si `Ax=b` tiene solución exacta, el punto más cercano es `b` mismo.

**Cita:** (*Sección 9.0*, p.440-441)

## 9.1 — Proyección ortogonal a múltiples vectores

### 9.1.1 — Ortogonal a un set

**Definición 9.1.1:** `v` es ortogonal a un set `S` si es ortogonal a cada vector de `S`.

**Lemma 9.1.3:** `v` ortogonal a `a1,...,an` ⟺ `v` ortogonal a todo `Span{a1,...,an}` (por linealidad del inner product — Lemma 8.3.2). Consecuencia: se difumina la distinción entre "ortogonal a un espacio" y "ortogonal a sus generadores".

### 9.1.2 — Proyección sobre/ortogonal a un vector space

**Definición 9.1.4:** para vector `b` y vector space `V`: `b = b‖V + b⊥V`, con `b‖V ∈ V` y `b⊥V` ortogonal a todo `V`.

**Lemma 9.1.6 (Generalized Fire Engine Lemma):** el punto en `V` más cercano a `b` es `b‖V`, y la distancia es `||b⊥V||`. Prueba: misma idea que Cap 8, vía Pitágoras — `b-p = (b-b‖V) + (b‖V-p)`, primer sumando es `b⊥V` (⊥ a V), segundo vive en V, split ortogonal → `||b-p||² = ||b⊥V||² + ||b‖V-p||²` → cualquier `p≠b‖V` da distancia estrictamente mayor.

**Cita:** (*Sección 9.1, Lemma 9.1.6*, p.441-443)

### 9.1.3 — Primer intento (falla)

Spec de `project_orthogonal(b, vlist)`: proyección de `b` ortogonal a `Span(vlist)`.

**Intento 1 — resta secuencial:**
```python
def project_orthogonal(b, vlist):
  for v in vlist:
    b = b - project_along(b, v)
  return b
```
**Falla** cuando vlist no es mutuamente ortogonal: contraejemplo `vlist=[[1,0],[√2/2,√2/2]]`, `b=[1,1]` → resultado final `[-1/2,1/2]` no es ortogonal a `[1,0]` (el paso 2 reintroduce componente que el paso 1 ya había eliminado, porque los dos vectores de vlist no son ⊥ entre sí).

**Intento 2 — batch (`classical_project_orthogonal`):** suma todas las proyecciones primero, resta una sola vez al final. También falla — peor, resultado no ortogonal a NINGÚN vector del vlist.

**Conclusión:** ambos intentos naive asumen implícitamente que vlist es mutuamente ortogonal. Sin esa condición, no hay solución simple por resta directa.

**Cita:** (*Sección 9.1.3*, p.443-445)

## 9.2 — Proyección con vlist mutuamente ortogonal

**Idea (Example 9.2.1):** si `v2 ⊥ v1`, la proyección de `b` a lo largo de `v2` (múltiplo escalar de `v2`) también es ⊥ `v1`. Restar algo ⊥ `v1` de algo que ya es ⊥ `v1` preserva la ortogonalidad. Prueba formal: `<v1, b-σv2> = <v1,b> - σ<v1,v2> = 0 + 0 = 0`.

**Cambio de spec** (en vez de arreglar el código): `project_orthogonal(b, vlist)` solo se garantiza correcto si vlist es **mutuamente ortogonal**. Bajo esa restricción, el Intento 1 (resta secuencial) SÍ es correcto.

### 9.2.1 — Prueba de correctness (loop invariant)

**Theorem 9.2.3:** para vlist mutuamente ortogonal, `project_orthogonal(b,vlist)` devuelve `b⊥` tal que `b⊥` ⊥ vlist Y `(b - b⊥) ∈ Span(vlist)`.

**Lemma 9.2.4 (loop invariant):** sea `k=len(vlist)`. Tras `i` iteraciones, `bi` es ortogonal a los primeros `i` vectores de vlist, y `b - bi ∈ Span` de esos primeros `i`.

**Prueba por inducción:**
- Caso base `i=0`: trivial (vacuamente cierto).
- Paso inductivo: `bi = bi-1 - αi·vi` donde `αi = <bi-1,vi>/<vi,vi>`. `bi ⊥ vi` por construcción. `bi ⊥ vj` (`j<i`): `<bi,vj> = <bi-1,vj> - αi<vi,vj> = 0 - αi·0 = 0` (primer término 0 por hipótesis inductiva, segundo 0 por mutua ortogonalidad de vlist). Y `b-bi = (b-bi-1) + αi·vi` ∈ span de los primeros `i` vectores.

Al llegar a `i=k`: `b⊥` es ortogonal a TODO vlist — cumple la spec.

**Bonus numérico (Problem 9.2.5):** `project_orthogonal` y `classical_project_orthogonal` son matemáticamente equivalentes (misma respuesta con aritmética exacta), pero en floating-point la versión clásica (suma-todo-luego-resta) acumula más error numérico que la secuencial.

**Cita:** (*Sección 9.2-9.2.1*, p.445-448)

### 9.2.2 — Augmented: `aug_project_orthogonal`

Extiende `project_orthogonal` para devolver también los coeficientes usados en cada paso — no solo `b⊥`.

**Ec 9.3/9.5:** `b = σ0·v0 + σ1·v1 + ... + σk-1·vk-1 + 1·b⊥` — identidad exacta: `b` se reconstruye combinando vlist más lo que sobró (`b⊥`).

```python
def aug_project_orthogonal(b, vlist):
    sigmadict = {len(vlist): 1}       # coef de b⊥ siempre es 1
    for i, v in enumerate(vlist):
        sigma = (b*v)/(v*v) if v*v > 1e-20 else 0
        sigmadict[i] = sigma
        b = b - sigma*v
    return (b, sigmadict)
```

`sigmadict` no es solo debug — son las coordenadas de `b` en la base ortogonal. Esto prepara la forma matricial de la Ec 9.4: `b = [v0|...|vk-1|b⊥] · [σ0,...,σk-1,1]`.

**Detalle floating-point:** umbral `v*v > 1e-20` (no `!= 0`) — mismo patrón que Cap 8, evita explotar con vectores casi-cero.

**Cita:** (*Sección 9.2.2*, p.448-449)

## 9.3 — Gram-Schmidt: construir generadores ortogonales

**El problema real:** todo lo anterior asume vlist YA mutuamente ortogonal — supuesto raro. Falta convertir cualquier lista arbitraria en una lista mutuamente ortogonal que genera el MISMO span.

**Problema de orthogonalization:**
- input: `[v1,...,vn]` cualquiera
- output: `[v1*,...,vn*]` mutuamente ortogonales, `Span{v1*,...,vn*} = Span{v1,...,vn}`

### 9.3.1 — El procedure (esto ES Gram-Schmidt)

```python
def orthogonalize(vlist):
  vstarlist = []
  for v in vlist:
    vstarlist.append(project_orthogonal(v, vstarlist))
  return vstarlist
```

Cada iteración proyecta `vi` ortogonal a lo ya acumulado en `vstarlist` (que, por construcción del paso anterior, ya es mutuamente ortogonal — así `project_orthogonal` sigue siendo válido en cada paso: el algoritmo se auto-alimenta).

**Lemma 9.3.1** (inducción simple usando Theorem 9.2.3): durante toda la ejecución, `vstarlist` es mutuamente ortogonal.

**Ejemplo 9.3.2:** `v1=[2,0,0], v2=[1,2,2], v3=[1,0,2]` → `v1*=[2,0,0]`, `v2*=[0,2,2]`, `v3*=[0,-1,1]`.

**Ejemplo 9.3.3** (cierra el problema abierto de 9.0.5/9.1.5): `v1=[8,-2,2], v2=[4,2,4]` → `orthogonalize` da `[[8,-2,2],[0,3,3]]` — ahora sí se puede correr `project_orthogonal` sobre este par.

**Cita:** (*Sección 9.3-9.3.1*, p.450-451)

### 9.3.2 — Prueba de correctness: preserva el span

No alcanza con mutua ortogonalidad — falta probar que el span no cambia.

**Lemma 9.3.5 (loop invariant):** tras `i` iteraciones, `Span(vstarlist) = Span{v1,...,vi}`.

**Prueba (inducción):** por hipótesis, `Span{v1*,...,vi-1*} = Span{v1,...,vi-1}`. Agregando `vi` a ambos lados: `Span{v1*,...,vi-1*,vi} = Span{v1,...,vi-1,vi}`. Falta `Span{...,vi*} = Span{...,vi}` — sale de la **Ec 9.6**: `vi = σ1i·v1* + ... + σi-1,i·vi-1* + vi*`, que muestra que `vi` y `vi*` son intercambiables para generar el mismo span (cualquier combinación con uno se reescribe con el otro).

Este proceso completo se llama **Gram-Schmidt orthogonalization** (Jørgen Pedersen Gram, Erhard Schmidt).

**Remark 9.3.6 — el orden importa:** `orthogonalize` sobre una lista y su reverso NO dan resultados espejados (cada `vi*` depende de la cascada de todo lo anterior). Contraste: `project_orthogonal(b, vlist)` SÍ da resultado único sin importar el orden de vlist — la proyección ortogonal a un espacio es un objeto matemático único.

**Cita:** (*Sección 9.3.2, Lemma 9.3.5, Remark 9.3.6*, p.451-452)

### Forma matricial — el germen de QR

**Ec 9.7:**
```
[v1|v2|...|vn]  =  [v1*|v2*|...|vn*]  ·  R
```
- Matriz izquierda: vectores originales, columnas.
- Primera matriz derecha: los `v*` ortogonales (futura "Q" de QR, sin normalizar todavía).
- `R`: cuadrada, **upper-triangular**, 1s en la diagonal, `σij` arriba (`vi` solo se expresa en términos de `v1*,...,vi-1*,vi*` — nunca mira "hacia adelante", por eso sale triangular).

**Ejemplo 9.3.7:** con `vstarlist=[[2,0,0],[0,2,2],[0,-1,1]]`:
```
[v1|v2|v3] = [[2,0,0],[0,2,-1],[0,2,1]] · [[1,0.5,0.5],[0,1,0.5],[0,0,1]]
```

Falta normalizar las columnas de la primera matriz a norma 1 para tener la QR factorization completa (Sección 9.7, no cubierta aún).

**Cita:** (*Sección 9.3.2, Ec 9.7, Example 9.3.7*, p.452-453)

## 9.4 — Closest point in Span (combinando orthogonalize + project_orthogonal)

Ahora sí, algoritmo completo para el Computational Problem 9.0.4: el vector en `Span{v1,...,vn}` más cercano a `b`.

Por la Generalized Fire Engine Lemma (9.1.6): el vector más cercano es `b^||V`, y `b^||V = b - b^⊥V`. Dos formas equivalentes de calcular `b^⊥V`:

- **Método 1:** `orthogonalize([v1,...,vn])` → `[v1*,...,vn*]`. Después `project_orthogonal(b, [v1*,...,vn*])` → da `b^⊥V` directo.
- **Método 2 (atajo):** meter `b` DENTRO de la lista: `orthogonalize([v1,...,vn,b])` → en la última iteración, el paso interno de `orthogonalize` sobre `b` es exactamente `project_orthogonal(b,[v1*,...,vn*])` — mismos cálculos, un solo llamado.

**Ejemplo 9.4.1:** `v1=[8,-2,2]`, `v2=[4,2,4]` (de 9.3.3, `v1*=[8,-2,2]`, `v2*=[0,3,3]`), `b=[5,-5,2]`. Corriendo `project_orthogonal(b,[v1*,v2*])`:

```
b1 = b - (<b,v1*>/<v1*,v1*>)*v1* = [5,-5,2] - (3/4)*[8,-2,2] = [-1,-3.5,0.5]
b2 = b1 - (<b1,v2*>/<v2*,v2*>)*v2* = [-1,-3.5,0.5] - (-1/2)*[0,3,3] = [-1,-2,2]
```
`b^⊥V = [-1,-2,2]`, entonces `b^||V = b - b^⊥V = [5,-5,2]-[-1,-2,2] = [6,-3,0]` — punto más cercano de `Span{v1,v2}` a `b`.

**Cita:** (*Sección 9.4, Example 9.4.1*, p.453-455)

## 9.5 — Otros problemas resueltos con orthogonalize

**Proposition 9.5.1:** vectores mutuamente ortogonales no-nulos son linealmente independientes — gratis, sin verificación extra.

**Prueba:** sean `v1*,...,vn*` mutuamente ortogonales no-nulos. Supongamos `0 = α1v1* + ... + αnvn*`. Producto interno con `v1*` en ambos lados:
```
<v1*,0> = α1<v1*,v1*> + α2<v1*,v2*> + ... + αn<v1*,vn*> = α1||v1*||² + 0 + ... + 0
```
`<v1*,0>=0` y `v1*` no-nulo (`||v1*||²≠0`) → `α1=0`. Análogo para `α2,...,αn`. Conecta ortogonalidad con independencia lineal — dos conceptos que antes parecían separados.

### 9.5.1 — Computing a basis

`orthogonalize` NO exige que `vlist` sea independiente — si es dependiente, algún `vi*` sale el vector cero (ya no aporta info nueva). Tomando solo los `vi*` no-cero: por Prop 9.5.1 son independientes, y generan el mismo span → son una **base**.

```python
def find_basis(vlist):
    vstarlist = orthogonalize(vlist)
    return [v for v in vstarlist if v is not the zero vector]
```
Bonus, mismo algoritmo: cuenta de no-ceros = **rank**; si algún `vi*` sale cero, `vlist` original era **linealmente dependiente** (Computational Problem 5.5.5).

### 9.5.2 — Computing a subset basis

Mejora: en vez de la base hecha de `vi*` (vectores modificados), usar los `vi` **originales** en las mismas posiciones donde `orthogonalize` dio no-cero. Se ven más "reales" — útil para saber cuáles features originales son redundantes vs. cuáles forman la base real.

**Por qué funciona:** `project_orthogonal(v, vstarlist)` ignora efectivamente los vectores cero dentro de `vstarlist` (`σ*0=0`) — así que correr `orthogonalize` solo con los originales "sobrevivientes" da el mismo `vi*` en cada paso.

```python
def find_subset_basis(vlist):
    vstarlist = orthogonalize(vlist)
    return [vlist[i] for i in range(len(vlist)) if vstarlist[i] is not the zero vector]
```

### 9.5.3 — aug_orthogonalize

Extiende `orthogonalize` para devolver también los coeficientes completos — la matriz `R` de la Ec 9.7, explícita:

- input: `[v1,...,vn]`
- output: `([v1*,...,vn*], [u1,...,un])` tal que `[v1|...|vn] = [v1*|...|vn*]·[u1|...|un]`

```python
def aug_orthogonalize(vlist):
    vstarlist = []
    sigma_vecs = []
    D = set(range(len(vlist)))
    for v in vlist:
        (vstar, sigmadict) = aug_project_orthogonal(v, vstarlist)
        vstarlist.append(vstar)
        sigma_vecs.append(Vec(D, sigmadict))
    return vstarlist, sigma_vecs
```

### 9.5.4 — Rounding errors en la práctica

`find_basis`/`find_subset_basis` son correctos en teoría, pero en floating-point los vectores que "deberían" salir cero no salen exactamente cero (mismo problema de `project_along`, Cap 8). Solución: "prácticamente cero" si `||v||² < 1e-20` (mismo umbral ya usado en `aug_project_orthogonal`).

**Cita:** (*Sección 9.5-9.5.4*, p.455-458)

## 9.6 — Orthogonal complement

**Definición 9.6.1:** dado espacio `W` y subespacio `U`, el complemento ortogonal de `U` respecto a `W` es `V = {w ∈ W : w ortogonal a TODO vector de U}` — no un solo vector proyectado, sino TODO el subespacio que "le da la espalda" a U.

**Lemma 9.6.2:** V es subespacio de W (cerrado bajo suma/escalar — sale gratis de la linealidad del inner product).

**Ejemplo 9.6.3:** `U = Span{[1,1,0,0],[0,0,1,1]}` en R^4. Vectores de forma `[c,-c,d,-d]` son ortogonales a todo U → `V = Span{[1,-1,0,0],[0,0,1,-1]}`. Se confirma que es TODO V (no solo una parte) vía Dimension Principle: `dim U + dim V = dim W = 4`.

### 9.6.2 — Complemento ortogonal + suma directa

**Lemma 9.6.4:** `U ∩ V = {0}` (si algo está en los dos, es ortogonal a sí mismo → tiene que ser el vector cero).

**Lemma 9.6.5 (clave):** `U⊕V = W` siempre — cualquier `b` de W se parte en `b = b^||U + b^⊥U`, uno vive en U, el otro en V, juntos cubren TODO W sin solaparse. (En Cap 10 esta conexión define la wavelet basis para compresión de imágenes.)

### 9.6.3 — Normal a un plano en R^3

"Normal" = ortogonal. Plano `Span{u1,u2}` (dim 2 en R^3) → complemento ortogonal tiene dim `3-2=1` (Direct-Sum Dimension Corollary 6.3.9) → una sola línea, cualquier vector no-cero ahí sirve de normal. **Ejemplo 9.6.6:** de 9.4.1, `[-1,-2,2]` (ortogonal a `Span{v1*,v2*}`) es la normal; normalizada `[-1/9,-2/9,2/9]`.

### 9.6.4 — Conexión con null space / annihilator

`Null A` = complemento ortogonal de `Row A` (porque `Au=0` significa "u ortogonal a cada fila de A"). Y ya sabías (Cap 6) que `Null A = annihilator(Row A)` → **complemento ortogonal y annihilator son el MISMO concepto**. Annihilator Theorem reciclado: complemento ortogonal del complemento ortogonal = espacio original.

### 9.6.5 — Normal dado por ecuación

Plano `{[x,y,z] : [a,b,c]·[x,y,z]=d}` → por el Annihilator Theorem, la normal es directamente `[a,b,c]` (los coeficientes de la ecuación) — sin calcular nada extra.

### 9.6.6 — Computing the orthogonal complement (algoritmo)

Dado basis `u1,...,uk` de U y `w1,...,wn` de W: `orthogonalize(U_basis + W_basis)` (U primero). Los `n-k` vectores `w*` no-cero que sobran son automáticamente ortogonales a todo U — son la base del complemento ortogonal.

```python
def find_orthogonal_complement(U_basis, W_basis):
    vstarlist = orthogonalize(U_basis + W_basis)
    return [wstar for wstar in vstarlist[len(U_basis):] if wstar is not zero_vector]
```

**Ejemplo 9.6.7:** `U=Span{[8,-2,2],[0,3,3]}`, W = basis estándar R^3 → único vector de la base del complemento: `[1/9,2/9,-2/9]` (coincide con la normal de 9.6.6, signo opuesto).

**Cita:** (*Sección 9.6*, p.458-461)

## 9.7 — La QR factorization

Primera factorización de matrices del libro: `A = Q*R`, donde `Q` tiene columnas mutuamente ortogonales Y de norma 1 (**orthonormal** — Definition 9.7.1; matriz cuadrada con esta propiedad = "orthogonal matrix", terminología confusa pero es la convención), y `R` es triangular superior.

**Lemma 9.7.2:** si Q es column-orthogonal, `Q^T*Q = identidad` (cada columna consigo misma da norma²=1, con otra da 0 — literalmente la definición de identidad). **Corollary 9.7.3:** si Q es cuadrada (orthogonal matrix), su inversa es `Q^T` — gratis, sin el trabajo normal de invertir.

**Definition 9.7.4:** `A (m×n, m≥n) = Q*R`, Q column-orthogonal m×n, R triangular n×n.

### 9.7.3 — Requiere columnas independientes

La salida cruda de `orthogonalize` casi cumple la definición — falta normalizar (dividir columna j por `||vj*||`, compensar multiplicando fila j de R por `||vj*||`). Si algún `vj*` es cero, división por cero → se impone precondición: columnas de A deben ser LINEALMENTE INDEPENDIENTES. Consecuencia: diagonal de R nunca es cero (necesario para backward substitution), y `Col Q = Col A` (Lemma 9.7.5).

**Cita:** (*Sección 9.7*, p.461-464)

## 9.8 — Usando QR para resolver `Ax=b`

### 9.8.1-9.8.2 — Caso cuadrado

`Ax=b` → sustituyendo `A=QR`: `QRx=b` → multiplicando por `Q^T`: `Rx = Q^T*b` (usando `Q^T*Q=I`). Como R es triangular con diagonal no-cero, se resuelve con backward substitution.

```python
def QR_solve(A, b):
    Q, R = qr_factor(A)
    return triangular_solve para Rx = Q^T*b
```

**Theorem 9.8.1:** si A es cuadrada con columnas independientes, `QR_solve` da la solución EXACTA de `Ax=b` (prueba: multiplicando `R*x-hat=Q^T*b` por Q, usando que `Q*Q^T=I` cuando Q es cuadrada).

### 9.8.3-9.8.5 — Least-squares (A con más filas que columnas)

Si A tiene más filas que columnas, `Ax=b` generalmente NO tiene solución exacta (el sistema pide demasiado). **Computational Problem 9.8.2:** encontrar `x-hat` que MINIMICE `||Ax-b||` (el "residual vector").

**Lemma 9.8.3:** si Q es column-orthogonal basis de V, `Q^T*b` da las coordenadas de `b^||V` en la base de Q, y `Q*Q^T*b` da `b^||V` mismo.

**Resultado central:** el MISMO `QR_solve`, sin cambiar una línea de código, también resuelve el least-squares problem — porque `A*x-hat = Q*Q^T*b = b^||V` (por Lemma 9.7.5 + 9.8.3), que es exactamente el punto más cercano a b en Col(A).

**Cita:** (*Sección 9.8*, p.464-469)

## 9.9 — Aplicaciones de least-squares

- **9.9.1 Regresión lineal:** ajustar `f(x)=a+cx` a datos con ruido — armar `A` con filas `[1,xi]`, resolver least-squares. Error vertical (no distancia real, unidades distintas en cada eje); suma de cuadrados por 2 razones: manejable matemáticamente Y óptimo bajo ruido Gaussiano (mal si hay outliers — ahí entra "robust statistics").
- **9.9.2-9.9.3 Fitting a cuadrática (1D/2D):** mismo truco con columnas `[1,xi,xi²]` (o `[1,x,y,xy,x²,y²]` en 2D) — sirve para encontrar el centro EXACTO de un patrón (ej. tumor en imagen) con precisión sub-píxel. El problema sigue siendo LINEAL en las incógnitas aunque la curva ajustada no lo sea.
- **9.9.4-9.9.5 Más mediciones = mejor precisión, gratis:** con sistema cuadrado y datos ruidosos, el resultado sale alejado de la realidad. Agregando MÁS mediciones (sistema sobre-determinado, sin solución exacta) y resolviendo least-squares, el resultado se acerca mucho más al valor real — sin mejorar el instrumento de medición, solo agregando datos + el método correcto.
- **9.9.6 Cierra el círculo con el Lab 8.4 (ML, WDBC):** el objetivo del lab (`w` tal que `signo(a·w)` prediga diagnóstico) es exactamente el least-squares problem: `minimizar sum((bi - ai·w)²)`. QR le gana a gradient descent en velocidad Y en garantía de encontrar el óptimo real (gradient descent depende del step size). **Verificado empíricamente hoy:** en un dataset sintético (50 ejemplos, 3 features + ruido gaussiano), `QR_solve` y `gradient_descent` (3000 iteraciones) convergen a EXACTAMENTE los mismos coeficientes y la misma loss — pero QR corrió ~350x más rápido (0.0004s vs 0.14s).

**Cita:** (*Sección 9.9*, p.468-474)

## Por qué importa para ML/AI

Este capítulo generaliza `project_along` (Cap 8, least-squares de 1 variable) a proyección sobre el span de varios vectores — resuelve exacto lo que el Lab 8.4 (gradient descent en WDBC) resolvía por iteración. QR factorization (9.7-9.9) es la base real de `np.linalg.lstsq`/regresión lineal en la práctica: mismo problema, solución exacta en vez de iterativa. Deep learning sigue usando gradient descent porque su loss NO es cuadrática — el atajo exacto de álgebra lineal solo aplica a problemas lineales/cuadráticos como este.

## Implementación propia

`05-Projects/coding-the-matrix/src/coding_the_matrix/orthogonalization.py` — Cap 9 COMPLETO (9.0-9.9): `project_orthogonal`, `aug_project_orthogonal`, `orthogonalize`, `aug_orthogonalize`, `closest_point`, `find_basis`, `find_subset_basis`, `find_orthogonal_complement`, `qr_factor`, `QR_solve`. 46 tests en `tests/test_orthogonalization.py` (todos verdes, suite completo del proyecto: 204 passed, 2 skip por dataset externo).

Visualización 3D interactiva: `05-Projects/coding-the-matrix/src/coding_the_matrix/visualize_orthogonalize.py` — pasos de Gram-Schmidt en 3D (vectores originales vs. `v*`). Correr: `cd 05-Projects/coding-the-matrix && uv run python -m coding_the_matrix.visualize_orthogonalize`.

## Pendiente / próxima sesión

**Capítulo 9 completo (9.0-9.10).** Próximo: Cap 10 (o el siguiente ítem del roadmap phase_0 — ver `00-Meta/progress.json`).

## Ver también

- [[Coding-the-Matrix-Inner-Product]] — capítulo anterior (fire engine problem, caso de 1 vector)
- [[Coding-the-Matrix-Gaussian-Elimination]]
