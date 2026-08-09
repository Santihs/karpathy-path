---
tags: [phase-0, math, linear-algebra, coding-the-matrix, orthogonalization, gram-schmidt, projection, least-squares, qr-factorization]
status: learning
first_learned: 2026-08-09
last_reviewed: 2026-08-09
confidence: 2/5
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

## Por qué importa para ML/AI

Este capítulo generaliza `project_along` (Cap 8, least-squares de 1 variable) a proyección sobre el span de varios vectores — resuelve exacto lo que el Lab 8.4 (gradient descent en WDBC) resolvía por iteración. Gram-Schmidt es además la base de QR factorization (Sección 9.7-9.9), que se usa para resolver `Ax=b` y least-squares en la práctica (regresión lineal como aplicación directa, Sección 9.9.1).

## Pendiente / próxima sesión

- **Repasar 9.1-9.3** antes de avanzar — sesión marcada como densa, confianza baja (2/5).
- Continuar desde **9.4**: Computational Problem "closest point in span de muchos vectores" resuelto con `orthogonalize` + `project_orthogonal` combinados, luego 9.5 (basis, subset basis), 9.6 (orthogonal complement), 9.7-9.9 (QR factorization completa, least-squares, linear regression).

## Ver también

- [[Coding-the-Matrix-Inner-Product]] — capítulo anterior (fire engine problem, caso de 1 vector)
- [[Coding-the-Matrix-Gaussian-Elimination]]
