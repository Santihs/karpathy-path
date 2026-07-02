---
tags: [phase-0, math, linear-algebra, axler]
status: learning
first_learned: 2026-07-01
last_reviewed: 2026-07-01
confidence: 3/5
---

# Linear Algebra — Fundamentos formales (Axler)

Source: *Linear Algebra Done Right* (4th ed.), Sheldon Axler — PDF en `00-Meta/resources/axler-lado.pdf`

Esta nota separa el lado **formal/riguroso** (definiciones, teoremas, pruebas) de la intuición geométrica de 3b1b, que vive en [[Linear-Algebra-Basics]]. Acá va primero la explicación en palabras simples, después la fórmula (LaTeX), después la cita exacta al libro (número de teorema + página) — así podés saltarte el símbolo si ya entendiste la idea.

---

## 1. Subespacios (Sección 1C, p.18-24)

**Idea simple:** un subespacio es un "sub-mundo" dentro de tu espacio vectorial que se comporta igual de bien — sigue siendo cerrado bajo suma y escalado, y sigue teniendo el cero adentro. No es cualquier subconjunto: la mayoría de subconjuntos NO son subespacios.

**Las 3 condiciones que tiene que cumplir (Condición 1.34, p.22):**
1. El vector cero tiene que estar adentro.
2. Si sumás dos elementos del subespacio, el resultado tiene que seguir adentro.
3. Si escalás un elemento del subespacio, el resultado tiene que seguir adentro.

En fórmula:
$$0 \in U \qquad u,w \in U \implies u+w \in U \qquad a \in \mathbf{F},\, u \in U \implies au \in U$$

**Atajo mental que sirve siempre:** el conjunto de soluciones de una ecuación lineal **homogénea** (que da 0) es automáticamente un subespacio. Si la ecuación da un número distinto de 0, o tiene productos/potencias de variables, ya no es subespacio (casi siempre).

### Ejercicio resuelto — ¿cuáles de estos son subespacios de F³?

| Conjunto | ¿Subespacio? | Por qué |
|---|---|---|
| $x_1+2x_2+3x_3=0$ | Sí | Ecuación homogénea — el patrón de arriba aplica directo |
| $x_1+2x_2+3x_3=4$ | No | El cero no cumple la ecuación (da 0≠4) |
| $x_1x_2x_3=0$ | No | El cero sí cumple, pero al sumar dos soluciones el resultado puede fallar (ej. $(1,0,0)+(0,1,1)=(1,1,1)$, cuyo producto ya no es 0) |
| $x_1=5x_3$ | Sí | Reescribe como $x_1-5x_3=0$ — mismo patrón homogéneo |

---

## 2. Independencia lineal (Sección 2A, p.31-33)

**Idea simple:** una lista de vectores es "independiente" si ninguno es redundante — no podés construir ninguno de ellos combinando los demás. Si algún vector SÍ se puede armar con los otros (combinación lineal), la lista es "dependiente" — hay desperdicio.

**Caso más fácil de recordar — dos vectores:** son independientes si ninguno es simplemente el otro escalado (estirado/encogido/volteado). Geométricamente: no apuntan en la misma línea.

**Definición formal (2.15, p.32):** la única forma de combinar los vectores para dar 0 es usando puros ceros como coeficientes.

$$a_1v_1 + \cdots + a_mv_m = 0 \implies a_1 = \cdots = a_m = 0$$

**Ejemplo concreto:** $(1,2,-4)$ y $(7,-5,6)$ son independientes en $\mathbf{R}^3$ — ninguno es múltiplo del otro. Pero eso NO los convierte en base de todo $\mathbf{R}^3$ (ver sección 3 abajo) — con solo 2 vectores como mucho cubrís un plano, y $\mathbf{R}^3$ tiene 3 dimensiones. Les falta una dirección.

---

## 3. Bases (Sección 2B, p.39-43)

**Idea simple:** una base es la lista "perfecta" de vectores para describir un espacio — ni te sobra ni te falta ninguno. Tiene que cumplir 2 cosas a la vez:
1. Ser independiente (nada de sobra/redundante).
2. Cubrir todo el espacio (nada de falta — todo punto se puede armar con esta lista).

**Definición (2.26, p.39):**
$$\text{base de } V = \text{lista linealmente independiente que hace span de } V$$

**Ejemplo que ya conocés — base estándar:** $(1,0,...,0), (0,1,...,0), ..., (0,...,0,1)$ es la base "por defecto" de $\mathbf{F}^n$ — cada vector tiene un 1 en una posición y 0 en el resto (*Example 2.27(a)*, p.39).

**Dos formas de fallar, con ejemplos (Example 2.27, p.39):**

- **Falta cobertura:** $(1,2,-4), (7,-5,6)$ — independientes, pero no llegan a cubrir todo $\mathbf{R}^3$ (les falta un vector).
- **Sobra redundancia:** $(1,2), (3,5), (4,13)$ — cubre todo $\mathbf{R}^2$, pero uno de los 3 vectores es combinación de los otros dos (sobra uno).

---

## 4. Dimensión (Sección 2C, p.44-49)

**Idea simple — para developer:** `dim V` es como `len()` pero aplicado al espacio entero, no a un vector individual. Te dice cuántos "grados de libertad" tiene el espacio.

**El truco que lo hace válido:** un mismo espacio tiene MUCHAS bases distintas posibles, pero Axler prueba primero (Teorema 2.34, p.44) que **todas las bases del mismo espacio tienen el mismo largo**. Recién ahí define dimensión como ese largo (2.35, p.44) — si no fuera así, "dimensión" sería ambigua (dependería de qué base elegís, como si `len()` diera un número distinto según cómo represento la misma lista).

$$\dim V = \text{largo de cualquier base de } V$$

**Para qué sirve en la práctica — 4 atajos:**

| Situación | Qué te dice |
|---|---|
| U es subespacio de V | $\dim U \le \dim V$ — nunca puede ser "más grande" |
| Tenés $n$ vectores independientes y $\dim V = n$ | Ya es base automáticamente, no hace falta chequear que cubre todo |
| Tenés $n$ vectores que cubren V y $\dim V = n$ | Ya es base automáticamente, no hace falta chequear independencia |
| $\dim U = \dim V$ y U es subespacio de V | Entonces $U = V$ exactamente — no hay "casi todo el espacio" |

**Conexión directa con ML:** el `rank` de una matriz de pesos = dimensión de su espacio de salida efectivo. Si el rank es menor que la dimensión de salida esperada, la capa está perdiendo información (cuello de botella) — mismo concepto de null space/rank que ya viste con 3b1b, ahora con base formal.

---

## 5. Mapas lineales (Sección 3A, p.52-56)

**Idea simple:** un "mapa lineal" es una función entre espacios vectoriales que respeta las 2 operaciones básicas — sumar y escalar. Si metés la suma de dos cosas, tiene que dar lo mismo que sumar los resultados por separado. Si escalás antes o después de aplicar la función, da lo mismo.

**Definición (3.1, p.52):**
$$\text{Additividad: } T(u+v) = Tu+Tv \qquad\qquad \text{Homogeneidad: } T(\lambda v) = \lambda(Tv)$$

**Consecuencia importante (Teorema 3.10, p.56):** todo mapa lineal manda el vector cero al vector cero.
$$T(0) = 0$$

**Ojo con la trampa de secundaria:** $f(x) = mx+b$ (la "función lineal" que aprendiste en el cole) NO es lineal en este sentido si $b \neq 0$ — la traslación rompe que $T(0)=0$. En álgebra lineal formal, "lineal" es más estricto que en el lenguaje común.

### Ejercicio resuelto — ¿cuándo T es lineal?

$T: \mathbf{R}^3 \to \mathbf{R}^2$, $T(x,y,z) = (2x-4y+3z+b,\ 6x+cxyz)$. Probar que T es lineal $\iff b=c=0$.

**Por qué:**
- Si $b \neq 0$: calculando $T(0,0,0) = (b, 0) \neq (0,0)$ — viola 3.10 directo.
- Si $c \neq 0$: probando con $v=(1,1,1)$, $T(2v) \neq 2T(v)$ (el término cúbico $cxyz$ escala distinto que linealmente) — viola homogeneidad.
- Si $b=c=0$: queda $T(x,y,z)=(2x-4y+3z,\ 6x)$ — combinación lineal pura de coordenadas, cumple ambas condiciones por construcción.

**Conclusión:** T es lineal exactamente cuando no hay traslación ($b=0$) ni términos no-lineales como productos de variables ($c=0$).

> **Flag repaso (quiz 2026-07-01):** confundí cuál condición rompe qué — recordar: **b≠0 = traslación** (rompe $T(0)=0$), **c≠0 = curva/no-linealidad** (rompe homogeneidad, no traslación).

---

## Recomendación de recurso complementario

*Linear Algebra Done Right* es riguroso pero denso en símbolos (pruebas formales, notación abstracta). Para bajar la carga simbólica sin perder profundidad, complementar con:

**"Coding the Matrix" — Philip N. Klein** (Brown University). Diseñado para estudiantes de Computer Science: ejemplos en Python, aplicaciones directas (compresión de imágenes, grafos, códigos de corrección de errores, gráficos por computadora), mucho menos notación griega. Sitio con video-clases gratis: codingthematrix.com.

## Ver también

- [[Linear-Algebra-Basics]] — intuición geométrica (3b1b), sin pruebas formales
