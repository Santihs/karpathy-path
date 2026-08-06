---
tags: [phase-0, math, linear-algebra, coding-the-matrix, basis, span, compression, grow-shrink, minimum-spanning-forest, gf2, dimension, rank, kernel-image, annihilator]
status: learning
first_learned: 2026-07-17
last_reviewed: 2026-08-06
confidence: 4/5
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

---

## 3. Fundamental Questions 5.2.4/5.2.5 — unicidad y minimalidad

### 5.2.4 — unicidad de coordenadas

Dada base `{a1,...,an}` que genera `V`, cualquier `v` en `V` tiene **exactamente una** forma de escribirse como combinación lineal de la base.

Ejemplo `R^2`: `a1=(1,0)`, `a2=(0,1)`, `v=(3,5)`. Única solución `c1=3, c2=5`.

**Prueba de unicidad** (por qué): si dos combos `c1..cn` y `d1..dn` dieran el mismo `v`, restando:

```
(c1-d1)*a1 + ... + (cn-dn)*an = 0
```

Si `a1..an` son linealmente independientes (única solución de esa ecuación es que todos los coeficientes sean cero), entonces forzosamente `ci=di` para todo `i`. Verificado con `a1=(1,0)`, `a2=(0,1)`:

```
(c1-d1)*(1,0) + (c2-d2)*(0,1) = (c1-d1, c2-d2) = (0,0)  →  c1=d1, c2=d2
```

**Conclusión**: span → garantiza EXISTENCIA de al menos una representación. Independencia → garantiza UNICIDAD (una sola). Base = span + independencia = existencia + unicidad.

### 5.2.5 — minimalidad

Base = generating set **mínimo** — si sacás cualquier vector, deja de generar `V`.

Ejemplo de vector redundante: `a1=(1,0)`, `a2=(0,1)`, `a3=(1,1)`. `a3 = a1+a2` (dependiente). `{a1,a2,a3}` genera `R^2` pero no es base (no es mínimo) — se puede sacar `a3` sin perder span. Trivial-solution test: `x1=-1, x2=-1, x3=1` da `-a1-a2+a3=0`, solución no trivial → dependencia confirmada.

`{a1,a2}` solo: sacar cualquiera de los dos pierde una dimensión entera → mínimo → base.

**Ojo con la trampa intuitiva**: "dirección nueva" se compara contra el **Span acumulado**, no contra cada vector individual por separado. `a3=(1,1)` apunta visualmente distinto a `a1` y `a2`, pero como `Span({a1,a2})` ya es el plano entero, `a3` cae adentro — no aporta nada nuevo.

Por qué importa: coordenadas (Cap 5.1, `A*u=v`) y compresión con pérdida (Cap 5.2, k-sparse) solo tienen sentido si la representación es única Y sin redundancia.

---

## 4. Grow y Shrink — dos algoritmos para encontrar el generating set mínimo (5.3)

### 5.3.1 — Grow

```
def Grow(V):
    B = ∅
    repeat while possible:
        find a vector v in V that is not in Span(B), and put it in B
```

Para cuando no queda vector nuevo para agregar → `B` genera todo `V`. La regla "solo agregar si NO está en Span(B)" garantiza que cada vector agregado es automáticamente independiente de los anteriores (si fuera dependiente, ya estaría en el span) → `B` resultante es base, no solo generador.

**Example 5.3.1** (`R^3`, generadores estándar): `e1=[1,0,0]` se agrega, `e2=[0,1,0]` no está en `Span({e1})` (esa recta nunca llega a `y`) → se agrega, `e3=[0,0,1]` no está en `Span({e1,e2})` (ese plano nunca llega a `z`) → se agrega. Cualquier `v=(a,b,c)=a*e1+b*e2+c*e3` ya está en `Span(B)` → algoritmo para con `B={e1,e2,e3}`.

### 5.3.2 — Shrink (enfoque opuesto)

```
def Shrink(V):
    B = some finite set of vectors that spans V
    repeat while possible:
        find a vector v in B such that Span(B - {v}) = V, and remove v from B
```

**Example 5.3.2**: `v1=[1,0,0]`, `v2=[0,1,0]`, `v3=[1,2,0]`, `v4=[3,1,0]`. `v4=3v1+v2` → redundante, se saca. `v3=v1+2v2` → redundante, se saca. Queda `B={v1,v2}` — ninguno puede generar al otro solo → para.

> **Errata verificada** (ver [[klein-example-5-3-2-span-errata]]): el libro dice "Span B = R³" en este ejemplo, pero los 4 vectores tienen z=0 siempre → el span real es solo el plano xy (subespacio 2D), no R³ completo. Confirmado línea por línea contra el PDF fuente — es un lapsus del autor, no afecta la lógica del algoritmo.

**Nota clave**: Grow/Shrink son algoritmos ABSTRACTOS ("no especifican cómo se da el input, cómo se ejecuta cada paso, ni qué vector elegir en cada iteración") — esa libertad de elección se explota después para probar que el tamaño final siempre es el mismo (Exchange Lemma, próxima sección a estudiar).

### 5.3.3 — Cuando greedy falla (contraejemplo con grafos)

**Dominating set**: conjunto de nodos donde cada nodo del grafo está en el conjunto o es vecino de alguien en el conjunto. Aplicar Grow/Shrink acá puede terminar en una solución válida pero NO mínima — hay casos con una solución más chica que el greedy no encuentra, porque decide en cada paso "sin pensar en el futuro".

**Por qué Grow/Shrink SÍ funcionan perfecto para bases de espacios vectoriales (y para MSF, ver abajo) pero NO para dominating-set**: independencia lineal tiene una propiedad de intercambio (exchange property) rígida y algebraica — dependencias entre vectores son consistentes en todo el espacio. "Ser vecino de" en un grafo genérico no tiene esa estructura — es puramente combinatorio, sin regla algebraica detrás.

---

## 5. Minimum Spanning Forest y GF(2) (5.4)

### 5.4.1 — Definiciones

- **path**: secuencia de aristas `[{x1,x2},{x2,x3},...,{xk-1,xk}]`, de `x1` a `xk`.
- **spanning**: conjunto `S` de aristas es spanning para grafo `G` si para cada arista `{x,y}` de `G` hay camino x-a-y usando solo aristas de `S`. Mismo sentido de "spanning" que en álgebra lineal — preview explícito del libro.
- **forest**: conjunto de aristas sin ciclos.

**MSF (Minimum Spanning Forest)**: dado grafo `G` con pesos, hallar `B` (spanning + forest) de peso total mínimo. "Forest" y no "tree" porque el grafo puede tener componentes desconectadas de entrada — no hay forma de conectarlas, la solución sale en varios árboles.

### 5.4.2 — Grow/Shrink para MSF (= Kruskal)

**Grow**: ordenar aristas de menor a mayor peso, agregar cada una si sus 2 extremos NO están ya conectados por lo que hay en `B` (si ya están conectados, agregarla crearía ciclo).

**Shrink**: empezar con todas las aristas, de mayor a menor peso, sacar cada una si sacarla no desconecta nada (hay camino alternativo).

Ejemplo verificado (Brown University campus, pesos 2,3,4,5,6,7,8,9): Grow y Shrink llegan al MISMO conjunto final `{2,3,4,6,7}` — mismo peso total, aunque construidos en direcciones opuestas. Implementado y testeado en `05-Projects/coding-the-matrix/src/coding_the_matrix/msf.py` (`msf_grow`/`msf_shrink`).

### 5.4.3 — Formulación en álgebra lineal sobre GF(2)

Esto conecta literal (no análogo) MSF con Cap 5.3: cada arista `{x,y}` → vector indicador sobre el dominio de nodos, con `1` (`gf2.one`) en `x` e `y`, `0` en el resto.

**Suma de aristas de un camino cancela nodos intermedios** (aritmética GF(2): `1+1=0`): sumar los vectores de `{Keeney,Main}+{Main,Wriston}+{Wriston,Gregorian}` da el vector de `{Keeney,Gregorian}` — `Main` y `Wriston` aparecen 2 veces cada uno y se cancelan, quedan solo los 2 extremos del camino.

**Regla general**: un vector con 1's en `x,y` está en el Span de un grupo de aristas SI Y SOLO SI hay camino x-a-y usando esas aristas. "Span" (álgebra) = "conectividad" (grafos), literalmente la misma condición.

**Example 5.4.4**: Span de `{Pembroke,BioMed}, {Main,Wriston}, {Keeney,Wriston}, {Wriston,Gregorian}` SÍ contiene `{Main,Keeney}` (camino Main-Wriston-Keeney) pero NO `{Athletic,BioMed}` ni `{BioMed,Main}` (Athletic no tocado; BioMed y Main en componentes distintas).

**Example 5.4.5**: Span de `{Athletic,BioMed}, {Main,Keeney}, {Keeney,Wriston}, {Main,Wriston}` NO contiene `{Pembroke,Keeney}`, `{Main,Gregorian}` ni `{Pembroke,Gregorian}` — Pembroke y Gregorian nunca aparecen tocados por esas 4 aristas. Visual con grafo + trace real de la eliminación: [[07-Visuals/msf-span-example-5-4-5-2026-07-18.html]].

**Punchline**: la condición que Grow chequea ("¿extremos ya conectados?") y Shrink chequea ("¿siguen conectados sin esta arista?") son, literalmente, un test de pertenencia a Span — el mismo test que en vectores normales. Implementado reusando el mismo código: `basis.is_in_span()` (Cap 5.3, genérico sobre cualquier campo) es llamado sin cambios desde `msf.py` (Cap 5.4, sobre GF(2)) — no hace falta BFS ni union-find.

---

## Doubts Resolved
- [[span-de-vectores]] — qué es el span de un conjunto de vectores, por qué algunas imágenes quedan fuera.
- [[compresion-basis-jpeg-pruning-ml]] — cómo esta idea de Klein es literalmente JPEG y magnitude pruning en ML.
- [[klein-example-5-3-2-span-errata]] — "Span B = R³" en Example 5.3.2 es una errata del libro (verificada contra el PDF fuente).

## Implementación
- `05-Projects/coding-the-matrix/src/coding_the_matrix/basis.py` — `is_in_span`/`grow`/`shrink`, span-membership vía eliminación genérica (funciona igual sobre reales o GF(2)).
- `05-Projects/coding-the-matrix/src/coding_the_matrix/msf.py` — `edge_to_vec`/`msf_grow`/`msf_shrink`, reusa `basis.is_in_span` sin cambios.
- Tests: `tests/test_basis.py`, `tests/test_msf.py` (19 tests nuevos, 93 total pasan).

## 6. Linear Dependence — el álgebra detrás de Grow/Shrink (5.5.1–5.5.11)

### 5.5.1 — Superfluous-Vector Lemma

**Enunciado**: para cualquier set `S` y vector `v∈S`, si `v` puede escribirse como combinación lineal de los OTROS vectores de `S`, entonces `Span(S-{v}) = Span(S)` — sacar un vector redundante no cambia el span.

**Analogía dev — columna calculada en DB**: tabla `orders` con `subtotal, tax, shipping` y una 4ta columna `total = subtotal+tax+shipping`. Cualquier query que use `total` se puede reescribir sustituyendo la fórmula (find-and-replace + reagrupar coeficientes) sin usarla — por eso se puede borrar la columna sin perder ningún reporte posible.

**Prueba** (`S={v1,...,vn}`, `vn = α1v1+...+α(n-1)v(n-1)` — Eq 5.1): tomás `v` arbitrario en `Span(S)`, `v=β1v1+...+βnvn`. Sustituís `vn` por la Eq 5.1 y reagrupás por vector:

```
v = (β1+βn·α1)v1 + (β2+βn·α2)v2 + ... + (β(n-1)+βn·α(n-1))v(n-1)
```

`v` quedó escrito sin `vn` → está en `Span(S-{vn})`. Como `v` era arbitrario, vale para todo `Span(S)` → QED.

### 5.5.2 — Definición formal de dependencia lineal

`v1,...,vn` son **linealmente dependientes** si `0 = α1v1+...+αnvn` con algún `αi≠0` (combinación NO trivial). Si la ÚNICA combinación que da cero es la trivial (todos los α=0) → **independientes**.

- Example 5.5.3: `[1,0,0],[0,2,0],[2,4,0]` dependientes — `2[1,0,0]+2[0,2,0]-1[2,4,0]=[0,0,0]`.
- Example 5.5.4: `[1,0,0],[0,2,0],[0,0,4]` independientes — cada uno tiene una posición exclusiva no-cero (namespace separado), ninguna combinación no-trivial puede cancelar las 3 a la vez.

Restatement: Computational Problem 5.5.5 (testear dependencia) es la MISMA pregunta que Question 4.7.7 (¿null space de `A=[v1|...|vn]` tiene solo el vector cero?) = Question 3.6.5 (¿sistema homogéneo tiene solo solución trivial?) — mismo problema, tercer disfraz.

### 5.5.3 — Dependencia lineal en MSF = ciclo en el grafo

Suma GF(2) de aristas que forman un **ciclo** da el vector cero (cada nodo del ciclo aparece exactamente 2 veces → se cancela). Verificado con triángulo `Main-Keeney-Wriston` en el grafo de Brown:

```
                Main  Keeney  Wriston
{Main,Keeney}     1      1       0
{Keeney,Wriston}  0      1       1
{Main,Wriston}    1      0       1
suma (GF2)        0      0       0
```

Coeficientes `(1,1,1)` — no-trivial → dependientes. **Ciclo en grafo = dependencia lineal**, literal (Example 5.5.7). Converso: forest (sin ciclo) → vectores independientes.

Esto es la justificación formal de por qué Grow (5.4.2) rechaza una arista cuando sus extremos ya están conectados: agregarla cerraría ciclo = la haría dependiente = ya está en `Span(B)`.

### 5.5.4 — Propiedades: Lemma 5.5.8 (subset) y Lemma 5.5.9 (Span Lemma)

**Lemma 5.5.8**: subset de un set independiente es independiente. Prueba por contrapositivo: si `S` (subset) es dependiente, extendés la misma combinación no-trivial a `T⊇S` agregando coeficiente 0 a los vectores extra — sigue siendo no-trivial → `T` también dependiente.

*Analogía dev*: si 3 servicios de un `docker-compose.yml` tienen dependencia circular, agregar 5 servicios más sin tocar los primeros 3 no arregla el ciclo — agregar cosas nunca cura una dependencia existente.

**Lemma 5.5.9 (Span Lemma)** — el más importante, motor de `is_in_span()`: `vi` está en el span de los otros vectores **si y solo si** existe combinación `0=α1v1+...+αnvn` con `αi≠0` específicamente.

- Dirección 1 (span→dependencia): si `vi=α1v1+...+αnvn` (sin `vi`), pasás `vi` al otro lado → `0=α1v1+...+(-1)vi+...+αnvn` — coef de `vi` es `-1≠0`.
- Dirección 2 (dependencia→span): si `0=...+αivi+...` con `αi≠0`, despejás `vi` dividiendo por `-αi` → `vi` queda en términos de los demás.

En grafos: arista `e` está en el span de otras aristas ⟺ hay un ciclo formado por `e` + subset de esas otras.

**Por qué importa**: convierte "¿puedo escribir `vi` en términos de los otros?" (prueba y error) en "¿existe una dependencia que toque a `vi` con coef≠0?" — resoluble con eliminación gaussiana / sistema homogéneo. Es literalmente lo que `basis.is_in_span()` hace.

### 5.5.5 — Corollary 5.5.10: Grow siempre produce independencia

**Prueba por inducción** (loop invariant, igual que probar que un `set()` nunca tiene duplicados en cada iteración):
- Caso base `n=0`: vacío, trivialmente independiente.
- Paso inductivo: `vk` fue agregado porque `vk ∉ Span(v1,...,vk-1)` (regla de Grow). Por el Span Lemma (contrapositiva), eso fuerza `αk=0` en cualquier combinación-cero. Queda `0=α1v1+...+αk-1vk-1`, y por hipótesis inductiva (`v1..vk-1` ya independientes) todos esos α también son 0 → única combinación-cero es la trivial → `v1..vk` independientes.

Aplicación directa en `msf_grow`: el chequeo "¿hay camino x-a-y con aristas ya elegidas?" ES el chequeo de `Span(B)` — por este corolario, el resultado siempre queda independiente sin necesidad de detectar ciclos por separado.

### 5.5.6 — Corollary 5.5.11: Shrink siempre produce independencia

**Prueba por contradicción** (más natural que inducción porque Shrink termina en un punto fijo, no cuenta pasos): asumís que el resultado final `B` es dependiente → existe `0=α1v1+...+αnvn` con algún `αi≠0` → por Span Lemma (5.5.9), `vi` está en el span de los demás → por Superfluous-Vector Lemma (5.5.1), `Span(B-{vi})=Span(B)` → **Shrink debería haber sacado a `vi`**, contradice que `B` ya es el resultado final (Shrink paró = no queda nada para sacar). Contradicción → `B` es independiente.

*Analogía dev*: como probar que un dead-code-eliminator que corre hasta punto fijo no puede terminar dejando código muerto — si quedara, el linter habría tenido algo más para borrar, contradiciendo que ya paró.

**Pipeline completo del capítulo**: 5.5.1 (redundancia→se puede sacar) → 5.5.2 (define dependencia) → 5.5.3 (ciclos=dependencia en grafos) → 5.5.8 (subset hereda independencia) → 5.5.9 (test operacional span↔dependencia) → 5.5.10/5.5.11 (Grow y Shrink SIEMPRE terminan independientes). Es el fundamento matemático completo detrás de `basis.py`/`msf.py` y sus 19 tests.

## 7. Exchange Lemma (5.5)

**Setup**: `B` = base de `V` (independiente + genera V), `T` = otro conjunto de vectores independientes en `V`. La Exchange Lemma dice: podés reemplazar vectores de `B` por vectores de `T`, uno a uno, y `B` sigue generando `V` en cada paso — nunca falta candidato para reemplazar, **mientras `T` no se agote antes que `B`**.

**El argumento (por contradicción)**: si `|T| > |B|`, en algún punto se agotan los vectores de `B` (todos ya reemplazados por vectores de `T`) pero a `T` le sobra al menos un vector sin usar. Ese conjunto ya reemplazado sigue generando `V` (invariante del lema) → el vector sobrante de `T` está en el Span de los demás → es linealmente dependiente. Contradice que `T` es independiente. Por lo tanto: **`|T| ≤ |B|`** siempre que `T` sea independiente y `B` genere `V`.

**Punchline — por qué Grow/Shrink siempre dan el mismo tamaño**: tomá dos bases cualesquiera `B1`, `B2` de `V`. Cada una es independiente Y genera `V` simultáneamente. Aplicando el resultado de arriba en las dos direcciones:
- `B1` genera, `B2` independiente → `|B2| ≤ |B1|`
- `B2` genera, `B1` independiente → `|B1| ≤ |B2|`

Las dos desigualdades juntas → `|B1| = |B2|`. Cualquier corrida de Grow o Shrink, sin importar orden ni elección de vectores, termina con el mismo tamaño — no es coincidencia empírica, es esta prueba. Cierra la pregunta de 5.3.3: funciona para vectores (y MSF, por la formulación GF(2) de 5.4.3) porque independencia lineal tiene esta propiedad de intercambio rígida; dominating-set no tiene análogo algebraico, por eso greedy puede fallar ahí.

---

# Capítulo 6: Dimension (Klein) — sesión 2026-08-05/06

## 8. Morphing Lemma y Basis Theorem (6.1)

**Setup**: `S` = generadores de `V`, `B` = set independiente en `V`. **Morphing Lemma (6.1.1)**: `|S| ≥ |B|`.

**Basis Theorem (6.1.2) — todas las bases del mismo espacio tienen el mismo tamaño.** Prueba: aplicás Morphing Lemma cruzado — `S=B1,B=B2` da `|B1|≥|B2|`; `S=B2,B=B1` da `|B2|≥|B1|` → juntas fuerzan `|B1|=|B2|`. Esto es lo que hace que "dimensión" tenga sentido como concepto único, no dependiente de qué base elegiste.

**Theorem 6.1.3**: un set de generadores de `V` es el generador MÁS CHICO posible ⟺ es una base. Prueba en 2 partes: (1) si `T` es base, cualquier otro generador `S` tiene `|T|≤|S|` por Morphing Lemma → `T` ya es mínimo. (2) si `T` NO es base, es generador dependiente → algún vector de `T` está en el span de los otros (Linear-Dependence Lemma 5.5.9) → se puede sacar sin perder span (Superfluous-Vector Lemma 5.5.1) → `T` no era mínimo.

**La prueba del Morphing Lemma es algorítmica**, no solo existencial — se llama "Morphing" porque transforma `S` en un set que contiene todo `B`, manteniendo el mismo tamaño en cada paso: en cada iteración "inyecta" un vector de `B` y "eyecta" un vector de `S` (decidido por el Exchange Lemma de la sección 7 arriba). Inducción sobre `k=0..|B|`: `S_k` mantiene el span de `V`, mismo cardinality que `S`, y ya contiene `b1..bk`.

**Ejemplo visual (grafos, campus Brown)** — el mismo proceso de morphing aplicado a spanning forests: `S`=forest inicial, `B`=forest objetivo. Se van intercambiando aristas una por una (inyectar la nueva, eyectar la que cierra ciclo), preservando siempre la propiedad de spanning forest y el mismo número de aristas. Instancia concreta y visual del Basis Theorem — dos spanning forests distintos del mismo grafo siempre tienen el mismo número de aristas.

## 9. Dimensión y Rank (6.2)

**Definition 6.2.1**: dimensión de `V` = tamaño de cualquier base de `V`, notado `dim V`. Bien definida gracias al Basis Theorem. Ejemplos: `dim(R³)=3` (base estándar), `dim(F^D)=|D|` para cualquier campo `F` y set finito `D`.

**Rank (Definition 6.2.5)**: dado un set `S` cualquiera (no necesariamente independiente), `rank(S) = dim(Span S)` — cuántas direcciones realmente independientes hay en `S`, sin importar cuántos vectores redundantes tenga.

**Proposition 6.2.8**: `rank(S) ≤ |S|` siempre — no podés generar más dimensiones de las que metiste (consecuencia del Subset-Basis Lemma: todo set finito contiene una base para su span).

**Row rank / column rank (Definition 6.2.9)**: para una matriz `M`, row rank = rank de sus filas, column rank = rank de sus columnas. Ejemplo trabajado — `M=[[1,0,0],[0,2,0],[2,4,0]]`: fila 3 = 2·fila1+2·fila2 (dependiente) → row rank=2; columnas `[1,0,2],[0,2,4],[0,0,0]` — la 3ra es cero, las otras 2 independientes → column rank=2. Coinciden.

**Rank en grafos (6.2.2)**: rank de un "connected subgraph" `T` (set de edges donde cada par pertenece a algún path dentro de `T`) = número de nodos tocados por esas edges, menos uno. Un solo edge → rank 1. Un ciclo de 3 edges → rank 2 (no 3 — el ciclo resta uno por la dependencia lineal, ver sección 6 arriba). Con 2 connected subgraphs disjuntos, los ranks se suman.

**Cardinalidad de un espacio vectorial sobre GF(2) (6.2.4)**: si `dim V = d`, entonces `V` tiene exactamente `2^d` vectores — por la Unique Representation Lemma (cada vector tiene representación única en la base, `d` coeficientes binarios → `2^d` combinaciones).

**Superset-Basis Lemma (6.2.13)**: todo set independiente `A` en `V` se puede extender a una base completa de `V`. Prueba: correr Grow empezando desde `T=A` en vez de vacío. Como Grow nunca rompe independencia, y `V⊆F^D` con `D` finito garantiza (por Morphing Lemma) que `|B|≤|D|` siempre, el algoritmo no puede crecer para siempre → termina con una base que contiene `A` entero.

**Dimension Principle (Lemma 6.2.14)** — la pieza más útil del capítulo: si `V` es subespacio de `W`, entonces **(D1)** `dim V ≤ dim W`, y **(D2)** si además `dim V = dim W`, entonces `V = W` — no puede quedar espacio "de sobra". Ejemplo: `V=Span{[1,2],[2,1]}` — como esos 2 vectores son independientes, `dim V=2=dim(R²)` → por D2, automáticamente `V=R²` sin verificar vector por vector.

**Grow termina (6.2.7)**: consecuencia directa de D2 — cada iteración de Grow sube `rank(S)` en 1; en el momento que `dim(Span S)=dim(V)`, D2 fuerza `Span S=V` → el algoritmo para ahí.

**Rank Theorem (Theorem 6.2.20)**: **row rank = column rank, siempre, para cualquier matriz.** Prueba elegante — escribís `A=BU` donde `B`=base del column space (`r` vectores) y `U`=coordenadas de cada columna en esa base. Reinterpretando la misma ecuación por FILAS en vez de columnas, cada fila de `A` resulta combinación lineal de las filas de `U` → `row rank(A) ≤ r = column rank(A)`. Aplicás el mismo argumento a la transpuesta `Aᵀ` (intercambia el rol de filas/columnas) → da la desigualdad al revés → juntas fuerzan la igualdad.

**Simple authentication revisited (6.2.9)** — aplicación de seguridad: password = vector secreto `x̂` sobre GF(2). Protocolo desafío-respuesta: computadora manda `a` random, humano responde `a·x̂`. Si Eve espía `m` pares `(ai,bi)`, puede responder cualquier desafío en `Span{a1,...,am}` (combinación lineal aplicada a las respuestas conocidas). Con vectores aleatorios y `m>n`, probablemente `rank[a1,...,am]=n` (máximo) → `Span=GF(2)^n` completo → Eve responde CUALQUIER desafío. Peor: la password es solución de `A·x=b`; una vez `rank(A)=n`, `Null A` es trivial → solución única → Eve calcula la password exacta con un solver de sistema lineal. Verificado con código Python del libro usando `independence.rank(L)`.

## 10. Direct Sum (6.3)

**Definition 6.3.1**: si `U` y `V` (subespacios de `F^D`) comparten SOLO el vector cero, `U⊕V = {u+v : u∈U, v∈V}`. Si comparten algo más, es ilegal formar el direct sum. En Python: `{u+v for u in U for v in V}` — análogo al Cartesian product pero sumando en vez de tuplear.

**No es lo mismo que unión de conjuntos**: `U∪V` solo junta los elementos tal cual; `U⊕V` genera TODAS las combinaciones `u+v` posibles. Ejemplo trabajado en chat: `U=Span{[1,0]}` (eje x), `V=Span{[0,1]}` (eje y) en R² — comparten solo el origen → `U⊕V` = cualquier `[a,b]=a·[1,0]+b·[0,1]` = **todo R²**. Si en cambio `V=Span{[2,0]}` (misma línea que `U`, solo escalada), comparten TODA la línea, no solo el cero → direct sum ilegal.

**Lemma 6.3.6**: la unión de generadores de `V` y generadores de `W` genera `V⊕W`.

**Direct Sum Basis Lemma (6.3.8)**: la unión de una BASE de `U` y una BASE de `V` es base de `U⊕V` (no solo generador — también independiente, porque cualquier combinación-cero se separa en parte-U y parte-V, cada una forzada a cero por separado ya que solo comparten el 0, y de ahí por independencia de cada base individual).

**Direct-Sum Dimension Corollary (6.3.9) — la fórmula clave**: `dim(U) + dim(V) = dim(U⊕V)`. Usada después en la prueba del Kernel-Image Theorem.

**Unique decomposition (6.3.10)**: cualquier vector en `U⊕V` tiene representación única como `u+v` — no hay 2 formas distintas de descomponerlo.

**Subespacios complementarios (6.3.11)**: si `U⊕V=W`, se dicen complementarios. No son únicos — un plano en R³ tiene infinitas líneas complementarias posibles (cualquiera que no esté contenida en el plano). Proposition 6.3.15 garantiza que siempre existe al menos un complemento, vía Superset-Basis Lemma.

## 11. Dimension y funciones lineales — Kernel-Image Theorem (6.4)

**Objetivo del capítulo**: criterio limpio para saber cuándo una función lineal (o matriz) es invertible.

**6.4.1**: `f:V→W` invertible ⟺ one-to-one (kernel trivial) Y onto (`Im f=W`, equivalente a `dim(Im f)=dim(W)` por Dimension Principle).

**La subfunción invertible más grande (6.4.2)**: dado `f:V→W` no necesariamente invertible, se construye `f*:V*→W*` que SÍ es invertible, recortando dominio y codominio. `W*=Im(f)` (asegura onto). Se eligen preimágenes `v1..vr` de una base `w1..wr` de `W*`, `V*=Span{v1..vr}`. Se prueba que `f*` es onto, one-to-one, y que `v1..vr` es base de `V*` — todo por la misma técnica (aplicar `f`, usar independencia de la base `wi`).

**Kernel-Image Theorem (6.4.7) — EL teorema del capítulo:**

$$\dim(\text{Ker } f) + \dim(\text{Im } f) = \dim(V)$$

Prueba: se muestra primero `V = Ker(f) ⊕ V*` (Lemma 6.4.5 — comparten solo el 0 porque el kernel de `f*` ya es trivial; y todo `v∈V` se descompone como `(v-v*)+v*` con `v*∈V*` elegido tal que `f(v*)=f(v)`). Aplicando la fórmula de dimensión del direct sum (sección 10): `dim V = dim(Ker f) + dim(V*)`, y como `dim(V*)=r=dim(Im f)` (biyección vía `f*`), sale el teorema.

**Consecuencias — todo lo demás de 6.4 es aplicar este teorema:**

- **Invertibilidad revisitada (Theorem 6.4.8)**: `f` invertible ⟺ `dim(Ker f)=0` Y `dim(V)=dim(W)`.
- **Rank-Nullity Theorem (6.4.9)**: para `f(x)=Ax` con `A` de `n` columnas: `rank(A) + nullity(A) = n`.
- **Checksum revisited (6.4.6)**: aplicación práctica — probabilidad de que un error de transmisión pase desapercibido en un checksum de 64 bits es `1/2^64`, derivado de Rank-Nullity + la fórmula de cardinalidad `2^dim` (sección 9).
- **Matrix invertibility (Corollary 6.4.10)**: `A` invertible ⟺ cuadrada (`|R|=|C|`) Y columnas independientes.
- **Corollary 6.4.11**: la transpuesta de una matriz invertible es invertible (usa el Rank Theorem).
- **Corollary 6.4.12**: si `A,B` cuadradas y `BA=I`, entonces `A` y `B` son inversas mutuas — no hace falta verificar `AB=I` por separado.
- **Change of basis (6.4.8)**: la matriz `C` que convierte coordenadas entre 2 bases del mismo espacio es necesariamente cuadrada, porque toda base del mismo espacio tiene el mismo tamaño (Basis Theorem).

## 12. El Annihilator (6.5)

**Motivación**: 4 "Conversion Problems" entre representaciones de un espacio (span de generadores ↔ solution set de un sistema homogéneo). El Problem 1 (dado `A`, encontrar generadores del null space) resuelve los otros 3 como subrutina — el resto de 6.5 desarrolla la matemática que lo justifica.

**Definition 6.5.7**: annihilator de un subespacio `V` de `F^n`, escrito `V°`, = `{u∈F^n : u·v=0 para todo v∈V}` — todos los vectores perpendiculares a TODO `V`.

**Lemma 6.5.8**: si `a1..am` generan `V` y `A`=matriz con esos vectores como filas, `V°=Null(A)` — conecta directo annihilator con null space.

**Annihilator Dimension Theorem (6.5.13)**: `dim V + dim V° = n`. Prueba trivial una vez tenés Rank-Nullity: `A`=matriz cuyo row space es `V`, `V°=Null A` (por 6.5.8), `rank A + nullity A = n` es exactamente `dim V + dim V° = n`.

**Annihilator Theorem (6.5.15) — cierra el capítulo**: `(V°)° = V` — el annihilator del annihilator es el espacio original. Prueba: cada vector base de `V` está en `(V°)°` (por definición cruzada de perpendicularidad) → `V` es subespacio de `(V°)°`; aplicando el Annihilator Dimension Theorem dos veces (a `V` y a `V°`) y restando, `dim V = dim(V°)°` → por Dimension Principle (D2), son el mismo espacio.

**Por qué importa**: si tenés un algoritmo para "generadores→annihilator" (que es el Problem 1 disfrazado), aplicarlo 2 veces resuelve también el Problem 2 (generadores→sistema homogéneo) — 2 problemas que parecían distintos son, literalmente, el mismo problema aplicado dos veces, gracias a este teorema.

## 13. Implementación — `rank`, `is_independent`, `is_invertible`

Agregado a `05-Projects/coding-the-matrix/src/coding_the_matrix/basis.py`, reusando `grow()` ya existente:

```python
def rank(vectors):
    """rank(S) = dim(Span S) = tamaño de cualquier base para su span."""
    return len(grow(vectors))

def is_independent(vectors):
    """Independiente ⟺ nadie fue descartado por grow() ⟺ rank == cantidad."""
    return rank(vectors) == len(vectors)

def is_invertible(M):
    """Corollary 6.4.10: invertible ⟺ cuadrada Y columnas independientes."""
    rows, cols = M.D
    if len(rows) != len(cols):
        return False
    return is_independent(list(mat2coldict(M).values()))
```

Tests: `tests/test_basis.py` — 13 tests nuevos (106 total pasan), incluyendo el ejemplo del libro donde el MISMO patrón 0/1 es invertible sobre R pero NO sobre GF(2) (porque `1+1=0` cambia qué combinaciones dan cero).

## 14. Ejercicios resueltos (6.7)

**Problem 6.7.5 — row rank/column rank en 4 matrices:**

1. `[[1,2,0],[0,2,1]]`: filas independientes (ninguna múltiplo de la otra) → row rank=2. Columnas `[1,0],[2,2],[0,1]` — `col1,col3` bastan como base (col2 es combinación de ambas) → column rank=2. ✓
2. `[[1,4,0,0],[0,2,2,0],[0,0,1,1]]`: filas en forma escalonada (pivote nuevo en cada una) → row rank=3. Columnas triangulares con det≠0 → column rank=3. ✓
3. `[[1],[2],[3]]`: filas todas múltiplo de `[1]` → row rank=1. Columna única no-cero → column rank=1. ✓
4. `[[1,0],[2,1],[3,4]]`: `[1,0],[2,1]` ya generan F² completo → row rank=2. Columnas `[1,2,3],[0,1,4]` no son múltiplo entre sí → column rank=2. ✓

**Método general**: mirar filas primero (¿alguna es combinación obvia de las otras?), elegir columnas independientes buscando pivotes/ceros exclusivos — sin necesidad de eliminación gaussiana formal en matrices chicas.

**Problem 6.7.6 — `my_is_independent(L)`**: se pide sin loop, reusando `rank`. Es la definición operacional de independencia: nadie es redundante ⟺ `rank(L)=len(L)`. Implementado como `is_independent` arriba.

**Problem 6.7.12 — `is_invertible(M)`**: traduce directo el Corollary 6.4.10 a código — cuadrada + columnas independientes. El ejemplo pedagógico central del libro: la matriz `[[1,0,1],[0,1,1],[1,1,0]]` es invertible sobre R (det=-2≠0) pero NO sobre GF(2) (fila1+fila2=`[1,1,0]`=fila3, dependientes porque `1+1=0` en GF(2)) — mismo patrón de números, resultado opuesto, porque invertibilidad depende del campo, no solo de "qué números hay".

**Problem 6.7.8 — prueba en una línea**: si `dim V = n`, cualquier `n+1` vectores son dependientes. Consecuencia directa del Morphing Lemma: si `S`=base de `V` (`|S|=n`) y `B`=set independiente en `V`, `|S|≥|B|` → `n≥|B|`. `n+1` vectores independientes violarían eso directo.

## 15. Ejercicios de práctica — ronda 2026-08-06

6 problemas cortos, sin prueba formal, para fijar Cap 6. Resultado: 4/6 sin ayuda.

- **dim de un span (3 vectores)**: gap propio — asumí independencia sin chequear si algún vector era resta obvia de los otros (`v1-v2=v3`). Antes de contar vectores, probar combinaciones simples (suma/resta) primero.
- **rank de un set con vector escalar redundante**: correcto sin ayuda.
- **row rank = column rank en matriz 2×2 con filas proporcionales**: correcto sin ayuda.
- **Dimension Principle — cuándo un span NO es todo el espacio**: correcto sin ayuda.
- **Direct sum en R³, dimensión resultante (plano, no todo R³)**: correcto sin ayuda.
- **Kernel-Image Theorem — despejar dim(Ker f) dado dim(Im f)**: gap propio — contesté "2" en vez de aplicar la resta `dim(Ker f)=dim(dominio)-dim(Im f)=3-2=1`. Confundí con copiar `dim(Im f)` en vez de restar del dominio.

**Patrón de los 2 gaps**: ambos son de "no aplicar el paso mecánico" (chequear combinación lineal directa; restar en la fórmula del teorema) más que de no entender el concepto — la intuición estaba bien en los 4 correctos.

## Próximo
Klein Cap 7 — Gaussian elimination (próxima sesión).
