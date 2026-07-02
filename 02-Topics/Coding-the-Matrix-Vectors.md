---
tags: [phase-0, math, linear-algebra, coding-the-matrix, vectors]
status: learning
first_learned: 2026-07-01
last_reviewed: 2026-07-01
confidence: 2/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Coding the Matrix — Cap 2: The Vector (Klein)

Source: *Coding the Matrix* (1st ed.), Philip N. Klein — Capítulo 2 (p.79+)

## 1. Anécdota de apertura — Hamilton vs. Gibbs (intro Cap 2, p.79-80)

**Quaternions, versión rápida:** extensión de números complejos a 4D. En vez de $a+bi$ (2D), Hamilton definió $q=a+bi+cj+dk$ con 3 unidades imaginarias ($i,j,k$), donde $i^2=j^2=k^2=ijk=-1$. Multiplicación NO conmutativa: $ij=k$ pero $ji=-k$.

**Para qué servían:** representar rotaciones en 3D de forma compacta, sin el problema de "gimbal lock" de los ángulos de Euler. Todavía se usan en gráficos por computadora, motores de videojuegos, robótica, control aeroespacial.

**La anécdota del libro:** William Rowan Hamilton (prodigio — a los 5 años ya sabía griego, latín, hebreo) pasó años buscando cómo extender los complejos a 3D para modelar rotaciones. La solución le llegó caminando junto al canal Royal en Dublín — tan urgido que talló las ecuaciones definitorias en la piedra del puente Brougham para no olvidarlas.

**El giro:** Josiah Willard Gibbs (Yale) inventó una alternativa más simple — el *vector analysis* que usamos hoy (dot product, cross product, vectores como listas de números), sin la complejidad algebraica de los quaternions. Hubo pelea académica real: Peter Tait (alumno de Hamilton) llamó el trabajo de Gibbs "a sort of hermaphrodite monster". Al final, vector analysis ganó por ser más práctico — aunque quaternions nunca murieron (siguen siendo la mejor herramienta específicamente para rotaciones 3D).

**Por qué importa para nosotros:** todo lo que venimos estudiando (3b1b, Axler) es la rama de Gibbs — vectores como listas de números, con dot/cross product. Los quaternions son un camino paralelo que resurge cuando necesitás rotaciones 3D sin gimbal lock (ej. IMUs, motores de física, animación).

## 2. Qué es un vector — definición formal (2.1, p.80-81)

**Idea simple:** acá "vector" no es una flecha con dirección — es literalmente una tupla de números de un tamaño fijo, todos del mismo tipo (campo). El nombre viene del latín "carrier" (portador) — algo que mueve/lleva información de un lugar a otro.

**Definiciones (2.1.1, 2.1.2, p.81):**
- Un *4-vector sobre $\mathbf{R}$* = vector con 4 entradas, cada una un real.
- En general, *n-vector sobre $\mathbf{F}$* = vector con $n$ entradas, cada una en el campo $\mathbf{F}$. El conjunto de todos estos se denota $\mathbf{F}^n$.

$$\mathbf{F}^n = \{(x_1, ..., x_n) : x_i \in \mathbf{F} \text{ para cada } i\}$$

**Ejemplo (2.1.2, p.81):** el set de 4-vectores sobre $\mathbf{R}$ se escribe $\mathbf{R}^4$. Ojo con esta notación — se lee igual que $F^D$ (funciones de D a F, Cap 0). No es casualidad: el libro sugiere interpretar $\mathbf{F}^d$ directamente como shorthand de $\mathbf{F}^{\{0,1,...,d-1\}}$ — osea, el conjunto de todas las funciones que van de $\{0,1,...,d-1\}$ (los índices) a $\mathbf{F}$ (los valores). Un vector de $n$ entradas ES una función con dominio los índices $\{0,...,n-1\}$.

## 3. Los vectores son funciones (2.2, p.81)

**Idea simple — la conexión que cierra el círculo con Cap 0:** recordá la notación $F^D$ (conjunto de todas las funciones de D a F, de la sección anterior). Un vector $\mathbf{R}^4$ es literalmente una función con dominio $\{0,1,2,3\}$ y codominio $\mathbf{R}$ — cada índice (0,1,2,3) es un input, cada entrada del vector es el output correspondiente.

$$\mathbf{F}^n \equiv \mathbf{F}^{\{0,1,...,n-1\}}$$

Ejemplo: el vector $[3.14159, 2.718281828, -1.0, 2.0]$ ES la función:
$$0 \mapsto 3.14159,\quad 1 \mapsto 2.718281828,\quad 2 \mapsto -1.0,\quad 3 \mapsto 2.0$$

**Por qué importa para developer:** en código, esto justifica representar un vector como `dict` en vez de `list` cuando es disperso (sparse) — la mayoría de entradas son 0, guardás solo las que importan, como una función parcial. Ese es el próximo tema del capítulo (2.2.1-2.2.2, representación con dicts y sparsity).

---

## 4. Qué podemos representar con vectores (2.3, p.84-85)

**Idea central:** cualquier cosa que se pueda describir como "un mapeo de un ID a un valor" es un vector. El libro da 6 casos concretos:

**Binary string** — una key criptográfica de n bits (ej. `10111011`) es un n-vector sobre $GF(2)$: `[1,0,1,1,1,0,1,1]`. Permite analizar esquemas de cifrado con álgebra lineal.

**Attributes (atributos)** — cualquier registro de datos con features nombradas. Ejemplo directo de ML:
```python
Jane = {'age': 30, 'education level': 16, 'income': 85000}
```
Esto es LITERALMENTE un vector — cada atributo es una "coordenada". Base de cómo se representan datasets en ML (feature vectors).

**State of a system (estado de un sistema)** — snapshot de un sistema evolucionando en el tiempo. Ejemplo: población de países en un momento dado:
```python
{'China':1341670000, 'India':1192570000, 'US':308745538, ...}
```

**Probability distribution** — ya lo vimos en [[Probability-Fundamentals]]: una distribución es función de un dominio finito a reales, por lo tanto ES un vector. Conecta con Markov chains / PageRank (Cap 12 del libro).

**Image (imagen)** — una imagen blanco-y-negro de 1024×768 es una función de pares de píxeles $(i,j)$ a intensidad (número). El dominio es un producto cartesiano de índices — igual patrón que Example 0.3.2 de Cap 0 (multiplicación). Ejemplo 2.3.1: gradiente 4×8 representado como dict `{(0,0):0, (0,1):0, ..., (7,3):224}`, donde 0=negro, 255=blanco.

**Point in space (punto en el espacio)** — en Cap 1 los puntos del plano se representaban con números complejos; de acá en adelante se representan con vectores — generaliza a 3D y dimensiones más altas sin cambiar la idea.

**Por qué importa:** esta lista es la razón por la que "vector" en ML no significa "flecha geométrica" — significa "cualquier cosa indexable". Un embedding, una fila de un dataset, una imagen, un estado de red neuronal — todo es la misma estructura matemática.

---

## 5. Suma de vectores y traslación (2.4-2.4.1, p.86-87)

**Idea simple:** sumar vectores = sumar entrada por entrada (elemento a elemento), como hacer `zip` + `+` sobre dos listas. Geométricamente, sumar un vector fijo a un punto lo "traslada" (mueve sin rotar ni escalar).

**Definición (2.4.1, p.86):**
$$[u_1,u_2,...,u_n] + [v_1,v_2,...,v_n] = [u_1+v_1,\ u_2+v_2,\ ...,\ u_n+v_n]$$

**Código (p.86):**
```python
def add2(v, w):
    return [v[0]+w[0], v[1]+w[1]]
```

**Traslación como función:** en Cap 1 la traslación en el plano complejo era $f(z)=z_0+z$ (sumar un complejo fijo). Acá es la misma idea con vectores: $f(\mathbf{v}) = \mathbf{v}_0 + \mathbf{v}$ — sumar un vector fijo $\mathbf{v}_0$ mueve cualquier input la misma distancia y dirección.

### Ejercicio resuelto (Quiz 2.4.2, p.86-87)

**Enunciado:** escribir "ir 1 milla al este y 2 millas al norte" como función de 2-vectores a 2-vectores, y aplicarla a $[4,4]$ y $[-4,-4]$.

$$f(\mathbf{v}) = [1,2] + \mathbf{v}$$

$$f([4,4]) = [1+4,\ 2+4] = [5,6]$$
$$f([-4,-4]) = [1+(-4),\ 2+(-4)] = [-3,-2]$$

**Por qué el vector es un "carrier" (portador):** el vector $[1,2]$ literalmente "lleva" un punto a otro — de $[4,4]$ a $[5,6]$, o de $[-4,-4]$ a $[-3,-2]$. Esto conecta directo con el origen etimológico de "vector" (latín para "carrier") mencionado en la sección 2.

---

## 6. Suma generalizada, vector cero, asociatividad/conmutatividad (2.4.1-2.4.2, p.87-88)

**Suma generalizada a n dimensiones (Quiz 2.4.4, p.87):**
```python
def addn(v, w): return [x+y for (x,y) in zip(v,w)]
# equivalente:
def addn(v, w): return [v[i]+w[i] for i in range(len(v))]
```

**Vector cero ($\mathbf{0}$, p.87):** todo campo $\mathbf{F}$ tiene elemento cero, así que $\mathbf{F}^D$ siempre tiene un vector con todas las entradas en 0. $f(\mathbf{v})=\mathbf{v}+\mathbf{0}$ es la traslación que no mueve nada — el "no-op" de la suma, mismo rol que la función identidad (Cap 0) o la matriz identidad (más adelante).

**¿Por qué es asociativa y conmutativa?** No hace falta probarlo aparte — la suma de vectores se DEFINE en términos de suma de entradas, y la suma en cualquier campo $\mathbf{F}$ (reales, complejos, GF(2)) ya es asociativa y conmutativa. La propiedad se hereda automáticamente:

$$\text{Asociatividad: } (x+y)+z = x+(y+z) \quad \text{(en el campo)}$$
$$\text{Conmutatividad: } x+y = y+x \quad \text{(en el campo)}$$

**Proposición 2.4.5 (p.87-88):** por lo tanto, para cualquier vectores $\mathbf{u},\mathbf{v},\mathbf{w}$:

$$(\mathbf{u}+\mathbf{v})+\mathbf{w} = \mathbf{u}+(\mathbf{v}+\mathbf{w}) \qquad \mathbf{u}+\mathbf{v} = \mathbf{v}+\mathbf{u}$$

**En código, esto te garantiza:** no importa el orden en que sumes una lista de vectores, ni cómo agrupes las operaciones (`reduce`, loop secuencial, suma en paralelo) — el resultado siempre es el mismo. Base de por qué operaciones como `sum(vectors)` o reducciones paralelas en ML (gradient accumulation, por ejemplo) son seguras.

## 7. Vectores como flechas (2.4.3, p.88)

Igual que los números complejos se visualizan como puntos/flechas en el plano (Cap 1), los n-vectores sobre $\mathbf{R}$ se visualizan como flechas en $\mathbf{R}^n$. El 2-vector $[3, 1.5]$ = flecha con cola en el origen $(0,0)$ y cabeza en $(3, 1.5)$ — o, equivalentemente, cualquier flecha paralela con la misma longitud y dirección (ej. cola en $(-2,-1)$, cabeza en $(1, 0.5)$). Misma idea que la intuición geométrica de 3b1b en [[Linear-Algebra-Basics]] — acá formalizada como "cualquier representación con el mismo desplazamiento es el mismo vector".

### Visualización — suma como "tip-to-tail" (p.89-90)

**Idea:** pa dibujar $\mathbf{u}+\mathbf{v}$, ponés la COLA de la flecha de $\mathbf{v}$ exactamente en la CABEZA de la flecha de $\mathbf{u}$. La suma es la flecha nueva que va desde la cola de $\mathbf{u}$ hasta la cabeza de $\mathbf{v}$ (línea punteada en el diagrama del libro).

```
        u+v (punteado)
         ↗
        /  ↑ v
       /  /
      / u/
     /  /
    0 ─────────→
```

**Interpretación (p.89-90):** la traslación que corresponde a $\mathbf{u}$ se COMPONE con la traslación que corresponde a $\mathbf{v}$ pa dar la traslación de $\mathbf{u}+\mathbf{v}$ — es literal composición de funciones (Cap 0, sección 0.3.5), aplicada a traslaciones.

### Ejercicio resuelto (2.4.7, p.90) — dibujar $[-2,4]+[1,2]$

$$[-2,4]+[1,2] = [-1,6]$$

**Cómo se vería:**
1. Flecha $\mathbf{u}=[-2,4]$: cola en $(0,0)$, cabeza en $(-2,4)$.
2. Flecha $\mathbf{v}=[1,2]$: cola puesta en $(-2,4)$ (la cabeza de $\mathbf{u}$), cabeza en $(-2+1,\ 4+2)=(-1,6)$.
3. Flecha suma (punteada): cola en $(0,0)$, cabeza en $(-1,6)$ — conecta directo el inicio de $\mathbf{u}$ con el final de $\mathbf{v}$.

---

## 8. Multiplicación escalar-vector (2.5, p.90-91)

**Idea simple:** "escalar" un vector = multiplicar cada entrada por el mismo número. En Cap 1, escalar un complejo por un real $r$ hacía $f(z)=rz$ (estiraba/encogía, y si $r<0$ además rotaba 180°). Acá es la versión vectorial de esa misma operación. Un "scalar" es solo un elemento del campo (un número) — se llama así porque su trabajo es "escalar" (agrandar/achicar) un vector.

**Definición (2.5.1, p.90):**
$$\alpha[v_1,v_2,...,v_n] = [\alpha v_1,\ \alpha v_2,\ ...,\ \alpha v_n]$$

**Ejemplo (2.5.2, p.90):** $2[5,4,10] = [2\cdot5,\ 2\cdot4,\ 2\cdot10] = [10,8,20]$

**Código (Quiz 2.5.3, p.90):**
```python
def scalar_vector_mult(alpha, v):
    return [alpha*v[i] for i in range(len(v))]
```

**Precedencia de operadores (p.91):** igual que en aritmética normal (multiplicación antes que suma), escalar-vector multiplicación tiene precedencia sobre suma de vectores. Sin paréntesis, se resuelve primero el escalado:

$$2[1,2,3]+[10,20,30] = [2,4,6]+[10,20,30] = [12,24,36]$$

**Por qué importa pa developer:** esta es la operación detrás de `learning_rate * gradient` en descenso de gradiente — escalás el vector gradiente por un número chico antes de restarlo de los pesos. Misma regla de precedencia aplica: $w - \alpha \nabla L$ significa "escalar el gradiente primero, restar después", no al revés.

---

## 9. Combinaciones convexas (2.6.1-2.6.3, p.94-97)

**Contexto — segmentos que no pasan por el origen (2.6.1, p.94-95):** un segmento del origen a $\mathbf{v}$ se describe fácil: $\{\alpha\mathbf{v} : \alpha\in[0,1]\}$. Pa un segmento que NO pasa por el origen (ej. de $[0.5,1]$ a $[3.5,3]$), lo trasladás sumando un offset fijo: $\{\alpha[3,2]+[0.5,1] : \alpha\in[0,1]\}$ — funciona, pero es asimétrico: un extremo aparece explícito, el otro solo se ve cuando $\alpha=1$.

**El arreglo — dos leyes distributivas (2.6.2, p.96-97):**
$$\text{Prop. 2.6.3: } \alpha(\mathbf{u}+\mathbf{v}) = \alpha\mathbf{u}+\alpha\mathbf{v}$$
$$\text{Prop. 2.6.5: } (\alpha+\beta)\mathbf{u} = \alpha\mathbf{u}+\beta\mathbf{u}$$

Reescribiendo con estas dos leyes, la fórmula del segmento queda simétrica:
$$\alpha[3.5,3] + \beta[0.5,1] \quad \text{donde } \beta = 1-\alpha$$

**Definición — combinación convexa (2.6.3, p.97):** una expresión $\alpha\mathbf{u}+\beta\mathbf{v}$ con $\alpha,\beta\ge0$ y $\alpha+\beta=1$.

$$\{\alpha[3.5,3]+\beta[0.5,1] : \alpha,\beta\in\mathbf{R},\ \alpha,\beta\ge0,\ \alpha+\beta=1\}$$

**Para qué sirve:** es la fórmula general de "interpolar linealmente entre dos puntos, repartiendo peso". $\alpha=1,\beta=0$ → estás en $\mathbf{u}$. $\alpha=0,\beta=1$ → estás en $\mathbf{v}$. Intermedio → punto ponderado entre ambos.

**Dónde reaparece (dev/ML):**
- **Lerp** (linear interpolation) en gráficos/animación.
- **Mixup** (data augmentation en deep learning): $\lambda x_1+(1-\lambda)x_2$ — misma fórmula exacta.
- **Softmax/attention weights**: no-negativos y suman 1 — cualquier promedio ponderado con esos pesos es combinación convexa de los value vectors.

### Ejemplo que lo hace click — promediar caras (Example 2.6.10, p.??)

Tomá dos vectores que representan IMÁGENES (cada píxel = una entrada del vector, ver sección 4 de esta nota) — una foto de cara $\mathbf{u}$ y otra $\mathbf{v}$. Con $\alpha=\beta=\frac{1}{2}$:

$$\frac{1}{2}\mathbf{u} + \frac{1}{2}\mathbf{v} = \text{promedio pixel-a-pixel de las dos imágenes}$$

Resultado: una tercera "cara" que es literal el promedio visual de las dos — mezcla de rasgos de ambas, a mitad de camino. Si generalizás variando $\alpha$ de 0 a 1 (con $\beta=1-\alpha$), obtenés una secuencia de imágenes que hace una transición suave (*morph*) de una cara a la otra — eso ES el "segmento de línea" entre las dos imágenes, ahora bien tangible: no es geometría abstracta, es directamente algo que podés ver.

**Por qué esto conecta todo:** confirma que "vector" y "combinación convexa" no son solo conceptos de flechas en el plano — aplican igual a CUALQUIER cosa representable como vector (imágenes, embeddings, datasets) — exacto lo que vimos en la sección 4 ("Qué podemos representar con vectores").

---

## Ver también

- [[Coding-the-Matrix-Fundamentals]] — funciones, notación $F^D$ (prerequisito directo de esta nota)
- [[Linear-Algebra-Axler-Fundamentals]] — versión formal/rigurosa (Axler)
- [[Linear-Algebra-Basics]] — intuición geométrica (3b1b)
