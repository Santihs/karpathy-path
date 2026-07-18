---
tags: [phase-0, math, linear-algebra, coding-the-matrix, basis, span, compression, grow-shrink, minimum-spanning-forest, gf2]
status: learning
first_learned: 2026-07-17
last_reviewed: 2026-07-18
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

## Próximo
Klein Cap 5.5 — Exchange Lemma: por qué Grow/Shrink en espacios vectoriales siempre terminan con el mismo tamaño (mínimo), sin importar el orden/elección de vectores — cierra por qué greedy funciona acá y en MSF pero falla en dominating-set (5.3.3).
