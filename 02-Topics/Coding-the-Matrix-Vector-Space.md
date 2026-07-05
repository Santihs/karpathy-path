---
tags: [phase-0, math, linear-algebra, coding-the-matrix, vector-space]
status: learning
first_learned: 2026-07-04
last_reviewed: 2026-07-04
confidence: 3/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Coding the Matrix — Cap 3: The Vector Space (Klein)

Source: *Coding the Matrix* (1st ed.), Philip N. Klein — Capítulo 3

## 1. Combinación lineal — definición (3.1.1, p.144)

**Idea simple:** dados vectores $v_1,...,v_n$, una combinación lineal es tomar cada uno, escalarlo por un coeficiente propio $\alpha_i$, y sumar todo.

$$\alpha_1\mathbf{v_1} + \cdots + \alpha_n\mathbf{v_n}$$

$\alpha_1,...,\alpha_n$ son los *coeficientes* — $\alpha_1$ es el coeficiente de $v_1$, etc.

### Ejemplo resuelto (3.1.2, p.144)

$-5[2,3.5] + 2[4,10]$

Paso 1 — escalar cada vector por su coeficiente:
- $-5\cdot[2,3.5] = [-10,-17.5]$
- $2\cdot[4,10] = [8,20]$

Paso 2 — sumar:
$$[-10,-17.5]+[8,20] = [-2,\ 2.5]$$

**Combinación trivial:** $0[2,3.5]+0[4,10] = [0,0]$ — coeficientes todos cero siempre dan el vector cero, para cualquier lista de vectores. Caso degenerado pero importante (reaparece en independencia lineal más adelante).

## 2. Usos de combinaciones lineales (3.1.2, p.144-145)

**Idea central:** una combinación lineal = "mezclar componentes por pesos y sumar el efecto total". Mismo objeto matemático, distinto significado según el dominio.

**Portfolios de acciones (Example 3.1.3):** sea $D$ el conjunto de acciones. Cada fondo mutuo $i$ = $D$-vector $\mathbf{v_i}$ (cuánto posee de cada acción por unidad de fondo). Si tenés $\alpha_i$ shares del fondo $i$, tu exposición real total a cada acción es:
$$\alpha_1\mathbf{v_1}+\cdots+\alpha_n\mathbf{v_n}$$

**Diseño de dieta (Example 3.1.4) — Stigler diet:** caso histórico real, EEUU años 1930s-40s. George Stigler (economista) quería dieta de costo mínimo cumpliendo requerimientos nutricionales de un soldado. 77 alimentos candidatos, 9 requerimientos nutricionales (calorías, proteína, calcio, hierro, vitaminas A/B1/B2/B3/C). Cada alimento $i$ = 9-vector $\mathbf{v_i}$ (cuánto aporta de cada nutriente por unidad). Dieta = cantidades $\alpha_i$ de cada alimento. Nutrición total entregada:
$$\alpha_1\mathbf{v_1}+\cdots+\alpha_{77}\mathbf{v_{77}}$$

Verificado (búsqueda web, 2026-07-04): Stigler (1945) resolvió a mano/heurístico (linear programming no existía aún) → dieta de 11¢/día (dólares 1939). Poco después, George Dantzig (inventor del simplex method, 1947) reconoció el problema de Stigler como caso temprano de LP; su equipo corrió el modelo exacto — 9 empleados con calculadoras manuales, 120 días-persona, confirmaron que la solución de Stigler era casi óptima. Caso histórico real de álgebra lineal → programación lineal (Cap 13 del libro cubre esto formalmente).

**Por qué conecta con [[Coding-the-Matrix-Vectors]] sección 9 (combinaciones convexas):** combinación convexa es combinación lineal con restricción extra ($\alpha_i\ge0$, $\sum\alpha_i=1$) — caso particular, no concepto nuevo.

## 3. Ejemplo — manufactura (bill of materials)

**Setup:** dominio $D=$ {metal, concrete, plastic, water, electricity}. Cinco juguetes, cada uno representado como un Vec sobre $D$ = cuánto material consume **una unidad** de ese juguete (entradas faltantes = 0 implícito, Vec sparse):

```python
>>> D = {'metal','concrete','plastic','water','electricity'}
>>> v_gnome  = Vec(D, {'concrete':1.3, 'plastic':.2, 'water':.8, 'electricity':.4})
>>> v_hoop   = Vec(D, {'plastic':1.5, 'water':.4, 'electricity':.3})
>>> v_slinky = Vec(D, {'metal':.25, 'water':.2, 'electricity':.7})
>>> v_putty  = Vec(D, {'plastic':.3, 'water':.7, 'electricity':.5})
>>> v_shooter= Vec(D, {'metal':.15, 'plastic':.5, 'water':.4, 'electricity':.8})

>>> print(240*v_gnome + 55*v_hoop + 150*v_slinky + 133*v_putty + 90*v_shooter)

 plastic metal concrete water electricity
-----------------------------------------
    215    51      312    373         356
```

**Qué es la combinación:** coeficientes (240, 55, 150, 133, 90) = cuántas unidades de cada juguete fabricás. La combinación lineal $240\mathbf{v_{gnome}}+55\mathbf{v_{hoop}}+150\mathbf{v_{slinky}}+133\mathbf{v_{putty}}+90\mathbf{v_{shooter}}$ da el vector de **materiales totales necesarios** para ese plan de producción.

**Verificación manual, columna por columna:**

- metal: $150(.25)+90(.15) = 37.5+13.5 = 51$ (solo slinky y shooter usan metal)
- concrete: $240(1.3) = 312$ (solo gnome usa concrete)
- plastic: $240(.2)+55(1.5)+133(.3)+90(.5) = 48+82.5+39.9+45 = 215.4\approx215$
- water: $240(.8)+55(.4)+150(.2)+133(.7)+90(.4) = 192+22+30+93.1+36 = 373.1\approx373$
- electricity: $240(.4)+55(.3)+150(.7)+133(.5)+90(.8) = 96+16.5+105+66.5+72 = 356$ (exacto)

**Por qué importa:** mismo patrón que portfolio/diet — cada producto = vector "consumo por unidad", coeficientes = cantidad producida, combinación lineal = recurso total agregado. Literal el **bill of materials (BOM)** de manufactura. Conecta con Cap.13 (LP): agregando costo por material y minimizando costo sujeto a demanda, es el mismo esqueleto que Stigler diet.

## 4. Implementación — lin_comb (Quiz 3.1.7, p.146)

**Idea (3.1.3, p.146):** de coeficientes a combinación lineal es función *forward* (fácil) — dado $[\alpha_1,...,\alpha_n]$ y $[\mathbf{v_1},...,\mathbf{v_n}]$, devolvés $\alpha_1\mathbf{v_1}+\cdots+\alpha_n\mathbf{v_n}$. El problema *backward* (dado el resultado, encontrar los coeficientes) es mucho más difícil — eso es resolver un sistema lineal, tema de capítulos más adelante.

**Implementado en `05-Projects/coding-the-matrix/src/coding_the_matrix/vecutil.py`:**
```python
def lin_comb(vlist, clist):
    return sum([coeff * v for (coeff, v) in zip(clist, vlist)])
```

Depende de `scalar_mul` (`coeff * v` → `Vec.__rmul__`) y `add` (`sum()` encadena `__add__`), ambos en `vec.py` — estaban con `raise NotImplementedError` desde el stencil original, implementados hoy junto con esto:

```python
def scalar_mul(v, alpha):
    return Vec(v.D, {k: alpha * getitem(v, k) for k in v.D})

def neg(v):
    return scalar_mul(v, -1)
```

Verificado con doctest — reproduce Example 3.1.2 (`lin_comb([[2,3.5],[4,10]], [-5,2]) == [-2,2.5]`) y suite completa de tests (`22 doctests + 16 pytest, todos pasan`).

## 5. Span (3.2.1, p.147-148)

**Definición (3.2.1):** el conjunto de TODAS las combinaciones lineales de $v_1,...,v_n$ se llama *span* de esos vectores, escrito $\text{Span}\{v_1,...,v_n\}$.

$$\text{Span}\{\mathbf{v_1},...,\mathbf{v_n}\} = \{\alpha_1\mathbf{v_1}+\cdots+\alpha_n\mathbf{v_n} : \alpha_1,...,\alpha_n \in \mathbf{F}\}$$

No es un vector — es un conjunto entero, generado variando los coeficientes sobre todos los valores posibles del campo. No "busca" ni "optimiza" nada — es resultado mecánico de variar coeficientes.

**Sobre campos infinitos (R, C):** span usualmente infinito (geometría de esto — rectas/planos por el origen — viene en próxima sección).

**Sobre campos finitos (GF(2)):** span también finito.

### Ejemplo resuelto (Quiz 3.2.2) — Span{[1,1],[0,1]} sobre GF(2)

Coeficientes $\alpha,\beta\in\{0,1\}$ → $2\times2=4$ combinaciones posibles:

$$0[1,1]+0[0,1]=[0,0]$$
$$0[1,1]+1[0,1]=[0,1]$$
$$1[1,1]+0[0,1]=[1,1]$$
$$1[1,1]+1[0,1]=[1,0]$$

4 combinaciones → 4 vectores distintos → span tiene 4 elementos = TODO GF(2)² (los únicos 4 2-vectors posibles sobre GF(2) son [0,0],[0,1],[1,0],[1,1]). Estos dos vectores cubren completamente el espacio 2D sobre GF(2).

**Span vs. base — la distinción clave:** span no busca nada, es el conjunto resultante de variar coeficientes. *Base* (ver [[Linear-Algebra-Axler-Fundamentals]] sección 3) sí tiene objetivo: la lista MÍNIMA cuyo span cubre el espacio completo, sin desperdicio (independencia lineal). En el ejemplo: {[1,1],[0,1]} da span completo de GF(2)² (tamaño $4=2^2$, dimensión 2) y ninguno de los dos vectores es combinación del otro (sin redundancia) → esta lista también es base de GF(2)².

## 6. Un sistema de ecuaciones lineales implica otras ecuaciones (3.2.2, p.150-151)

**Contexto (Example 3.2.7) — atacando el esquema de autenticación simple (visto en 2.9.6):** password secreto = vector $\hat{\mathbf{x}}$ sobre $GF(2)$. Server manda challenge $\mathbf{a}$, humano responde $\mathbf{a}\cdot\hat{\mathbf{x}}$.

Eve (eavesdropper) observó 3 pares challenge-respuesta:
$$\mathbf{a_1}=[1,1,1,0,0],\ \beta_1=1 \qquad \mathbf{a_2}=[0,1,1,1,0],\ \beta_2=0 \qquad \mathbf{a_3}=[0,0,1,1,1],\ \beta_3=1$$

**Pregunta:** ¿para qué otros challenges puede Eve derivar la respuesta correcta sin conocer $\hat{\mathbf{x}}$?

**Respuesta:** cualquier challenge en $\text{Span}\{\mathbf{a_1},\mathbf{a_2},\mathbf{a_3}\}$. 3 vectores, coeficientes $\alpha_i\in\{0,1\}$ → $2^3=8$ combinaciones → 8 vectores en el span (tabla completa en el libro, p.150).

**El truco — por qué funciona:** si $\mathbf{a}$ está en ese span, se escribe $\mathbf{a}=\alpha_1\mathbf{a_1}+\alpha_2\mathbf{a_2}+\alpha_3\mathbf{a_3}$. Entonces:

$$\mathbf{a}\cdot\hat{\mathbf{x}} = (\alpha_1\mathbf{a_1}+\alpha_2\mathbf{a_2}+\alpha_3\mathbf{a_3})\cdot\hat{\mathbf{x}}$$
$$= \alpha_1(\mathbf{a_1}\cdot\hat{\mathbf{x}})+\alpha_2(\mathbf{a_2}\cdot\hat{\mathbf{x}})+\alpha_3(\mathbf{a_3}\cdot\hat{\mathbf{x}}) \qquad \text{(distributividad + homogeneidad, sección 10.5)}$$
$$= \alpha_1\beta_1+\alpha_2\beta_2+\alpha_3\beta_3$$

Todo del lado derecho, Eve ya lo conoce (β son respuestas escuchadas) — no necesita $\hat{\mathbf{x}}$.

**Ejemplo concreto:** challenge $[1,0,1,0,1]=1\mathbf{a_1}+1\mathbf{a_2}+1\mathbf{a_3}$ (última fila de la tabla). Respuesta correcta $=1\beta_1+1\beta_2+1\beta_3=1+0+1=0$.

**Generalización (p.150-151):** si $\hat{\mathbf{x}}$ satisface $m$ ecuaciones lineales $\mathbf{a_i}\cdot\mathbf{x}=\beta_i$ ($i=1,...,m$), podés calcular $\mathbf{a}\cdot\hat{\mathbf{x}}$ para CUALQUIER $\mathbf{a}\in\text{Span}\{\mathbf{a_1},...,\mathbf{a_m}\}$ — sin resolver el sistema, sin conocer $\hat{\mathbf{x}}$. El sistema "implica" gratis todas esas ecuaciones extra. Conecta directo con Question 2.9.20 (¿un sistema de ecuaciones implica otras ecuaciones? sí — exactamente las del span de los vectores challenge).

**Limitación explícita (libro, p.151):** esto solo prueba que las ecuaciones del span SON implicadas — no prueba que sean las ÚNICAS implicadas (se demuestra en capítulo posterior).

**Ataque real (Example 3.2.8):** Eve rompe el esquema completo si $\text{Span}\{\mathbf{a_1},...,\mathbf{a_m}\} = GF(2)^n$ (todo el espacio de challenges posibles) — ahí responde CUALQUIER challenge, password ya no protege nada. Defensa: elegir challenges cuyo span no cubra todo el espacio.

## 7. Generators (3.2.3, p.151)

**Definición (3.2.9):** sea $\mathcal{V}$ conjunto de vectores. Si $\mathbf{v_1},...,\mathbf{v_n}$ son tal que $\mathcal{V}=\text{Span}\{\mathbf{v_1},...,\mathbf{v_n}\}$, decimos que $\{\mathbf{v_1},...,\mathbf{v_n}\}$ es un *generating set* para $\mathcal{V}$, y llamamos a $\mathbf{v_1},...,\mathbf{v_n}$ *generators* de $\mathcal{V}$.

**Ejemplo (3.2.10):** los 8 vectores GF(2) de la sección 6 (span del ataque a Eve) son exactamente $\text{Span}\{11100,01110,00111\}$ → esos 3 vectores son generating set del conjunto de 8.

**Ejemplo (3.2.11):** $\{[3,0,0],[0,2,0],[0,0,1]\}$ genera todo $\mathbf{R}^3$. Prueba en 2 partes:
1. Toda combinación lineal cae en $\mathbf{R}^3$ (obvio).
2. Todo $[x,y,z]\in\mathbf{R}^3$ se escribe como combinación de esos 3:
$$[x,y,z] = (x/3)[3,0,0]+(y/2)[0,2,0]+z[0,0,1]$$

## 8. Combinaciones de combinaciones (3.2.4, p.152)

**Idea:** otro generating set para $\mathbf{R}^3$: $\{[1,0,0],[1,1,0],[1,1,1]\}$. Se prueba escribiendo los generadores VIEJOS (ya confirmados) como combinación de los NUEVOS:

$$[3,0,0]=3[1,0,0]$$
$$[0,2,0]=-2[1,0,0]+2[1,1,0]$$
$$[0,0,1]=0[1,0,0]-1[1,1,0]+1[1,1,1]$$

**Por qué alcanza:** si los nuevos generan a los viejos, y los viejos ya generan todo $\mathbf{R}^3$, por transitividad los nuevos también generan todo $\mathbf{R}^3$ — sustituyendo cada viejo por su versión en términos de los nuevos, cualquier combinación de viejos se convierte en combinación de nuevos.

## 9. Standard generators (3.2.5, p.153-154)

**Fórmula más simple posible:** $[x,y,z]=x[1,0,0]+y[0,1,0]+z[0,0,1]$ — los coeficientes son literal las coordenadas del vector. Estos 3 vectores son los *standard generators* de $\mathbf{R}^3$, notados $\mathbf{e_0},\mathbf{e_1},\mathbf{e_2}$.

**Generaliza a $\mathbf{R}^n$:** $\mathbf{e_0},...,\mathbf{e_{n-1}}$, cada uno todo ceros salvo un 1 en posición $i$.

**Generaliza a cualquier dominio finito $D$ y campo $\mathbf{F}$:** para cada $k\in D$, $\mathbf{e_k}$ = función $\{k:1\}$ (mapea $k$ a 1, resto a 0). Generadores estándar de $\mathbf{F}^D$.

**Código (Quiz 3.2.13):**
```python
def standard(D, one):
    return [Vec(D, {k: one}) for k in D]
```
Parámetro `one` existe para soportar $GF(2)$ (el "1" de ese campo, no necesariamente el int de Python).

## 10. Geometría del span sobre R (3.3.1, p.155-157)

**Span de un vector no-cero $\mathbf{v}$:** $\text{Span}\{\mathbf{v}\}=\{\alpha\mathbf{v}:\alpha\in\mathbf{R}\}$ → recta por el origen y $\mathbf{v}$. Objeto 1-dimensional.

**Span del conjunto vacío:** solo el vector cero (combinación trivial) → un punto, objeto 0-dimensional.

**Span de dos vectores:** ¿plano? Depende de independencia. Ejemplo con $[1,0,1.65]$ y $[0,1,1]$ (independientes) → plano completo por el origen (visualizado con grid de puntos $\alpha\mathbf{u}+\beta\mathbf{v}$).

**Contraejemplo (Example 3.3.4):** $\text{Span}\{[1,2],[2,4]\}$ — $[2,4]=2[1,2]$, el segundo vector ya es múltiplo del primero:
$$\alpha_1[1,2]+\alpha_2[2,4] = \alpha_1[1,2]+\alpha_2(2[1,2]) = (\alpha_1+2\alpha_2)[1,2]$$
Sigue siendo solo múltiplos de $[1,2]$ → $\text{Span}\{[1,2],[2,4]\}=\text{Span}\{[1,2]\}$ = una recta, NO un plano. Vector redundante no agrega dimensión.

**Patrón general — "flats"** (objetos geométricos: puntos, rectas, planos e híper-versiones en más dimensiones):
- span de 0 vectores → punto (origen)
- span de 1 vector → recta por el origen, o punto (si el vector es cero)
- span de 2 vectores → plano por el origen, o recta, o punto (según independencia)

## 11. Geometría de soluciones de sistemas homogéneos (3.3.2, p.157-158)

**Forma alternativa de describir un plano:** no como span, sino como ecuación. Plano genérico $ax+by+cz=d$. Para que pase por el origen $(0,0,0)$, hay que forzar $d=0$.

**Definición (3.3.8):** ecuación lineal con lado derecho 0 se llama *homogénea* — mismo concepto que en [[Linear-Algebra-Axler-Fundamentals]] (subespacios = soluciones de ecuaciones homogéneas).

**Ejemplo (3.3.7):** el plano $\text{Span}\{[1,0,1.65],[0,1,1]\}$ se reescribe como
$$\{(x,y,z):1.65x+y-z=0\} \;=\; \{[x,y,z]:[1.65,1,-1]\cdot[x,y,z]=0\}$$
Mismo plano, dos representaciones: span (constructivo, genera desde vectores) vs. solución de ecuación homogénea (restrictivo, recorta desde el espacio completo).

**Ejemplo recta en R² (3.3.9):** recta $=\text{Span}\{[3,2]\}=\{[x,y]:2x-3y=0\}$. Misma recta, dos formas.

**Ejemplo recta en R³ (3.3.10):** acá una sola ecuación NO alcanza (una ecuación en $\mathbf{R}^3$ da un plano, no una recta) — se necesitan DOS ecuaciones homogéneas simultáneas:
$$\{[x,y,z]:[4,-1,1]\cdot[x,y,z]=0,\ [0,1,1]\cdot[x,y,z]=0\}$$
La recta es la intersección de dos planos — cada ecuación restringe una dimensión; dos restricciones en $\mathbf{R}^3$ dejan 1 dimensión libre.

**Patrón que se arma:** span y solución de sistema homogéneo son dos caras de la misma moneda — misma geometría, ángulos opuestos de describirla (generar vs. recortar).

## 12. Vector spaces — qué tienen en común span y solución homogénea (3.4.1, p.159)

**Objetivo:** cualquier subconjunto $\mathcal{V}\subseteq\mathbf{F}^D$ — sea span de vectores o solución de sistema lineal homogéneo — cumple 3 propiedades:

- **V1:** $\mathcal{V}$ contiene el vector cero.
- **V2:** cerrado bajo escalar — si $\mathbf{v}\in\mathcal{V}$, entonces $\alpha\mathbf{v}\in\mathcal{V}$ para todo escalar $\alpha$.
- **V3:** cerrado bajo suma — si $\mathbf{u},\mathbf{v}\in\mathcal{V}$, entonces $\mathbf{u}+\mathbf{v}\in\mathcal{V}$.

**Nota — ya visto antes:** son exactamente las 3 condiciones de subespacio de [[Linear-Algebra-Axler-Fundamentals]] sección 1 (Condición 1.34, p.22): $0\in U$, cerrado bajo suma, cerrado bajo escalar. Klein llega a lo mismo probándolo concretamente desde $\mathcal{V}=\text{Span}\{\mathbf{v_1},...,\mathbf{v_n}\}$, en vez de partir de axioma abstracto.

**Prueba para $\mathcal{V}=\text{Span}\{\mathbf{v_1},...,\mathbf{v_n}\}$:**

- V1: $0\mathbf{v_1}+\cdots+0\mathbf{v_n}$ = combinación trivial, siempre en el span.
- V2: si $\mathbf{v}=\beta_1\mathbf{v_1}+\cdots+\beta_n\mathbf{v_n}$, entonces $\alpha\mathbf{v}=\alpha\beta_1\mathbf{v_1}+\cdots+\alpha\beta_n\mathbf{v_n}$ — sigue siendo combinación lineal de los mismos generadores, sigue en el span.
- V3: si $\mathbf{u}=\alpha_1\mathbf{v_1}+\cdots+\alpha_n\mathbf{v_n}$ y $\mathbf{v}=\beta_1\mathbf{v_1}+\cdots+\beta_n\mathbf{v_n}$, entonces $\mathbf{u}+\mathbf{v}=(\alpha_1+\beta_1)\mathbf{v_1}+\cdots+(\alpha_n+\beta_n)\mathbf{v_n}$ — de nuevo combinación lineal de los mismos generadores.

**Por qué importa:** confirma que "span" y "subespacio" (Axler) describen el mismo objeto matemático desde ángulos distintos — span es la construcción explícita (generadores + combinaciones), subespacio es la propiedad abstracta que ese conjunto satisface.

**Prueba para $\mathcal{V}=\{\mathbf{x}:\mathbf{a_1}\cdot\mathbf{x}=0,\ ...,\ \mathbf{a_m}\cdot\mathbf{x}=0\}$ (solución de sistema homogéneo):**

- V1: $\mathbf{a_1}\cdot\mathbf{0}=0,\ ...,\ \mathbf{a_m}\cdot\mathbf{0}=0$ — el vector cero satisface trivialmente cualquier ecuación homogénea (dot product con cero siempre da cero).
- V2: si $\mathbf{a_1}\cdot\mathbf{v}=0,...,\mathbf{a_m}\cdot\mathbf{v}=0$, entonces por homogeneidad del dot-product (sección 10.5, Prop. 2.9.22) $\alpha(\mathbf{a_i}\cdot\mathbf{v})=\alpha\cdot0=0$ para cada $i$, o sea $\mathbf{a_i}\cdot(\alpha\mathbf{v})=0$ — $\alpha\mathbf{v}$ sigue siendo solución.
- V3: si $\mathbf{u}$ y $\mathbf{v}$ son ambos soluciones ($\mathbf{a_i}\cdot\mathbf{u}=0$ y $\mathbf{a_i}\cdot\mathbf{v}=0$ para cada $i$), entonces $\mathbf{a_i}\cdot\mathbf{u}+\mathbf{a_i}\cdot\mathbf{v}=0$, y por distributividad (Prop. 2.9.25) $\mathbf{a_i}\cdot(\mathbf{u}+\mathbf{v})=0$ — $\mathbf{u}+\mathbf{v}$ también es solución.

**Por qué importa — cierra el círculo:** las 3 propiedades algebraicas del dot-product que probamos en la sección 10.5 (homogeneidad, distributividad) son EXACTAMENTE lo que hace que el conjunto solución de un sistema homogéneo sea un subespacio — no es coincidencia, es la maquinaria que lo garantiza. Confirma que span (constructivo) y solución-homogénea (restrictivo) son dos caminos que llegan al mismo tipo de objeto: un vector space.

## 13. Subspaces (3.4.3, p.162)

**Definición (3.4.9):** si $\mathcal{V}$ y $\mathcal{W}$ son vector spaces y $\mathcal{V}\subseteq\mathcal{W}$, decimos que $\mathcal{V}$ es *subspace* de $\mathcal{W}$.

Un conjunto es subconjunto de sí mismo → $\mathcal{W}$ siempre es subspace de sí mismo (caso trivial).

**Ejemplos, cadena de contención:**
- $\{[0,0]\}$ (solo el cero) — su único subspace es él mismo (Example 3.4.10).
- $\{[0,0]\}$ es subspace de $\{\alpha[2,1]:\alpha\in\mathbf{R}\}$ (la recta que pasa por $[2,1]$), que a su vez es subspace de $\mathbf{R}^2$ (Example 3.4.11) — cadena: punto ⊂ recta ⊂ plano.
- $\mathbf{R}^2$ **NO** es subspace de $\mathbf{R}^3$ (Example 3.4.12) — $\mathbf{R}^2$ = conjunto de 2-vectors, $\mathbf{R}^3$ = conjunto de 3-vectors, ninguno de los 2-vectors está literalmente contenido en $\mathbf{R}^3$ (no es "el plano XY dentro del espacio 3D", es un conjunto de objetos de tipo distinto). Ojo con esta trampa — geométricamente uno visualiza $\mathbf{R}^2$ "adentro" de $\mathbf{R}^3$, pero formalmente no son subconjuntos, son espacios de dimensión distinta con vectores de tamaño distinto.

**Pregunta abierta (Example 3.4.13):** ¿qué vector spaces están contenidos en $\mathbf{R}^2$? El más chico es $\{[0,0]\}$ — jerarquía completa (punto → rectas por el origen → todo $\mathbf{R}^2$) queda para desarrollar.

## 14. *Abstract vector spaces (3.4.4, p.163) — nota conceptual, no examinable en el libro

**Tentación (que el libro NO valida formalmente):** decir que todo vector space = span de un número finito de vectores Y solución de sistema lineal homogéneo. Según matemática formal, **no es cierto en general**.

**Por qué:** en este libro, vector = función de dominio finito $D$ a campo $\mathbf{F}$ (definición concreta, ligada a estructura interna). Matemática moderna define las cosas por los AXIOMAS que satisfacen, no por su estructura interna (misma idea que "field" — no importa qué son los elementos, importa qué operaciones cumplen).

**Definición abstracta:** un *vector space* sobre campo $\mathbf{F}$ es cualquier conjunto $\mathcal{V}$ equipado con operación de *suma* y operación de *scalar-multiplication* (cumpliendo ciertos axiomas) que satisface Properties V1, V2, V3 (sección 12 de esta nota). Los elementos de $\mathcal{V}$, sean lo que sean, actúan como "vectores" — sin comprometerse a una estructura interna específica.

**Por qué esto importa — abre la puerta a objetos raros:** bajo esta definición, el conjunto de TODAS las funciones de $\mathbf{R}$ a $\mathbf{R}$ (dominio infinito, no finito) ES un vector space según la definición abstracta — algo que la definición concreta del libro (dominio finito) no cubre. Si un subspace de ESE espacio es span de un conjunto finito de vectores es pregunta matemática más profunda, fuera del alcance del libro.

**Por qué Klein elige NO usar el enfoque abstracto:** la noción concreta de vector (función de dominio finito) ayuda a construir intuición — es más fácil razonar con listas de números concretas que con axiomas puros. Pero el aviso es explícito: yendo más profundo en matemática, el enfoque abstracto es el estándar que vas a encontrar.

**Conexión con [[Linear-Algebra-Axler-Fundamentals]]:** Axler SÍ usa el enfoque abstracto desde el principio (vector space definido por axiomas, sección 1 del libro de Axler antes de siquiera hablar de $\mathbf{F}^n$) — Klein aquí está señalando explícitamente la diferencia de nivel de abstracción entre los dos libros que venimos usando en paralelo.

## 15. Affine spaces (3.5, p.164-169)

### 15.1 Flats que no pasan por el origen (3.5.1)

Ya vimos (sección 9, combinaciones convexas) que un segmento que no pasa por el origen se arma trasladando uno que sí pasa: $f([x,y])=[x,y]+[0.5,1]$. Pregunta: ¿cómo representar formalmente una recta/plano que NO pasa por el origen?

### 15.2 Affine combinations (3.5.2, Definition 3.5.2)

**Definición:** una combinación lineal $\alpha_1\mathbf{u_1}+\cdots+\alpha_n\mathbf{u_n}$ se llama *affine* si los coeficientes SUMAN exactamente 1: $\sum_i\alpha_i=1$.

**Ejemplo (3.5.3):** $2[10,20]+3[0,10]+(-4)[30,40]$ es afín porque $2+3+(-4)=1$.

**Conexión con combinaciones convexas (sección 9):** convexa = afín + restricción extra de que todos los coeficientes sean $\ge0$. Afín es la versión más permisiva (coeficientes pueden ser negativos, solo importa que sumen 1).

### 15.3 Affine spaces (3.5.3, Definition 3.5.8)

**Definición:** un *affine space* es el resultado de trasladar un vector space. Formalmente: $\mathcal{A}$ es affine space si existe vector fijo $\mathbf{a}$ y vector space $\mathcal{V}$ tal que
$$\mathcal{A}=\{\mathbf{a}+\mathbf{v}:\mathbf{v}\in\mathcal{V}\} \qquad\text{i.e. } \mathcal{A}=\mathbf{a}+\mathcal{V}$$

**Dato que cierra el círculo:** un *flat* (sección 10 de esta nota — recta/plano/etc.) es literal un affine space que vive dentro de $\mathbf{R}^n$. "Flat" y "affine space" son el mismo concepto — flat es el caso concreto en $\mathbf{R}^n$.

**Ejemplo (3.5.9):** el plano por $\mathbf{u_1}=[1,0,4.4]$, $\mathbf{u_2}=[0,1,4]$, $\mathbf{u_3}=[0,0,3]$ se escribe como $\mathbf{u_1}+\text{Span}\{\mathbf{u_2}-\mathbf{u_1},\mathbf{u_3}-\mathbf{u_1}\}$ — como ese span ES un vector space, el plano completo es un affine space (traslación del span por $\mathbf{u_1}$).

**Lemma 3.5.10 — la pieza que conecta todo:** para cualquier vectores $\mathbf{u_1},...,\mathbf{u_n}$:
$$\left\{\alpha_1\mathbf{u_1}+\cdots+\alpha_n\mathbf{u_n} : \sum_{i=1}^n\alpha_i=1\right\} = \{\mathbf{u_1}+\mathbf{v} : \mathbf{v}\in\text{Span}\{\mathbf{u_2}-\mathbf{u_1},...,\mathbf{u_n}-\mathbf{u_1}\}\}$$

En palabras: el *affine hull* (todas las combinaciones afines posibles) de un grupo de puntos = tomar $\mathbf{u_1}$ como ancla, sumarle cualquier vector del span de las diferencias respecto a $\mathbf{u_1}$.

**Prueba (ida):** cualquier vector del span de la derecha es $\alpha_2(\mathbf{u_2}-\mathbf{u_1})+\cdots+\alpha_n(\mathbf{u_n}-\mathbf{u_1})$. Sumando $\mathbf{u_1}$ y reagrupando (homogeneidad + distributividad):
$$(1-\alpha_2-\cdots-\alpha_n)\mathbf{u_1}+\alpha_2\mathbf{u_2}+\cdots+\alpha_n\mathbf{u_n}$$
Coeficientes suman exactamente 1 (el primero es 1 menos la suma de los demás) → es combinación afín.

**Prueba (vuelta):** dada combinación afín con $\sum\alpha_i=1$, se despeja $\alpha_1=1-\alpha_2-\cdots-\alpha_n$ y se reconstruye la misma forma → está en el lado derecho.

**Consecuencia:** el affine hull de cualquier conjunto de vectores es siempre un affine space.

### 15.4 Representando affine space como solución de sistema lineal NO homogéneo (3.5.4)

Ya vimos (sección 11) que flat CON origen = solución de sistema homogéneo (lado derecho 0). Ahora: flat SIN origen = solución de sistema con lado derecho DISTINTO de cero.

**Ejemplo plano (3.5.11):** el mismo plano por $\mathbf{u_1},\mathbf{u_2},\mathbf{u_3}$ de arriba también es
$$\{[x,y,z]\in\mathbf{R}^3 : [1.4,1,-1]\cdot[x,y,z]=-3\}$$
mismo plano, descrito ahora como ecuación no homogénea (lado derecho $-3$).

**Ejemplo recta (3.5.12):** la recta por $[0.5,1]$ y $[3.5,3]$ (todas sus combinaciones afines) también es
$$\{[x,y]\in\mathbf{R}^2 : [2,-3]\cdot[x,y]=-2\}$$

**Patrón que se completa:** span (por el origen) ↔ solución homogénea (lado derecho 0). Affine hull (NO por el origen) ↔ solución no homogénea (lado derecho ≠0). Combinación lineal genera vector spaces; combinación afín (coeficientes suman 1) genera affine spaces — versión trasladada del mismo objeto.

## Doubts Resolved

- Stigler diet: historia verificada — ver fuentes [Wikipedia](https://en.wikipedia.org/wiki/Stigler_diet), [History of the Diet Problem](http://www.statslab.cam.ac.uk/~rrw1/opt/diet_history.html)

## Ver también

- [[Coding-the-Matrix-Vectors]] — Cap 2, prerequisito directo (vectores, suma, escalar, combinaciones convexas)
- [[Linear-Algebra-Axler-Fundamentals]] — versión formal/rigurosa (Axler)
