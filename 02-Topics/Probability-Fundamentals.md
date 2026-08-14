---
tags: [phase-0, math, probability, coding-the-matrix, mml-book]
status: learning
first_learned: 2026-07-01
last_reviewed: 2026-08-14
confidence: 3/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
source_pdf_2: "mml-book.pdf (Deisenroth/Faisal/Ong) — https://mml-book.github.io/book/mml-book.pdf"
---

# Probabilidad — Fundamentos (Klein Cap 0.4)

Source: *Coding the Matrix* (1st ed.), Philip N. Klein — Sección 0.4 (p.12-18)

**Status del roadmap:** `probability_distributions_expectation` y `probability_cross_entropy_softmax` siguen `not_started` en Phase 0 — esta nota es el arranque (prob. discreta básica), falta expectation, cross-entropy y softmax en sesión dedicada.

## 1. Distribución de probabilidad discreta (0.4.1, p.12)

**Idea simple:** una distribución de probabilidad es un dict donde cada "resultado posible" (key) mapea a un número entre 0 y 1 (probabilidad), y todos los values suman exactamente 1. Igual que `F^D` de la sección anterior, pero acá el codominio son reales no-negativos con una restricción extra (suman 1).

**Definición formal:** $\Pr(\cdot)$ es una distribución de probabilidad discreta sobre dominio finito $\Omega$ (los *outcomes*) si:

$$\sum_{\omega \in \Omega} \Pr(\omega) = 1$$

**Ejemplos uniformes (todos los outcomes con igual probabilidad):**
- Moneda: `Pr = {'heads':1/2, 'tails':1/2}`
- Dado: `Pr = {1:1/6, 2:1/6, ..., 6:1/6}`
- 2 monedas: `Pr = {('H','H'):1/4, ('H','T'):1/4, ('T','H'):1/4, ('T','T'):1/4}`

**Ejemplo no-uniforme (Scrabble, p.13):** las letras no tienen igual probabilidad — hay que ponderar por cuántas fichas hay de cada letra. Truco: encontrás una constante $c$ tal que $\Pr[\text{letra } X] = c \cdot (\text{cantidad de fichas de } X)$, y resolvés $c$ con la restricción de que todo sume 1 (acá $c=1/95$, porque hay 95 fichas en total).

## 2. Eventos y suma de probabilidades (0.4.2, p.14)

**Idea simple:** un "evento" es simplemente un subconjunto de resultados que te interesan (ej. "sacar una vocal"). Su probabilidad = sumar las probabilidades de cada resultado que lo compone.

$$\Pr[\text{evento}] = \sum_{\omega \in \text{evento}} \Pr(\omega)$$

Ejemplo: $\Pr[\text{vocal}] = \Pr(A)+\Pr(E)+\Pr(I)+\Pr(O)+\Pr(U) = 9/95+12/95+9/95+8/95+4/95 = 42/95$.

## 3. Aplicar una función a un input aleatorio (0.4.3, p.14)

**Idea simple:** si metés un input aleatorio a una función, el output también es aleatorio — y podés calcular su distribución agrupando: para cada output posible, sumás las probabilidades de todos los inputs que lo producen (piensa en un `groupby` + `sum`).

Ejemplo: tirás un dado (uniforme, 1/6 cada cara), aplicás $f(x) = 0$ si par, $1$ si impar. Resultado: $\Pr[0]=\Pr[1]=1/2$ (3 caras pares, 3 impares, cada grupo suma 3×1/6).

## 4. Funciones invertibles preservan la forma de la distribución (0.4.3-0.4.5, p.15-18)

**Idea clave (la que conecta todo):** si la función que aplicás es **invertible** (ver [[Coding-the-Matrix-Fundamentals]] sección 4), cada output tiene EXACTAMENTE un input que lo produce — no hay que sumar nada, la probabilidad del output = probabilidad de su único input.

**Consecuencia poderosa:** si el input es uniforme y la función es invertible, el output también es uniforme. Ejemplo (0.4.9, p.16): cifrado César con key aleatoria uniforme → cyphertext también uniforme — el atacante no gana información con solo mirar la distribución del output.

**Aplicación — perfect secrecy (0.4.4-0.4.5, p.16-18):** un esquema de cifrado logra *secreto perfecto* si, para cada mensaje plano posible, la función de encriptación (con la key aleatoria) produce la MISMA distribución de output — así ver el cyphertext no le da a un atacante ninguna pista sobre cuál era el mensaje. Se logra construyendo la encriptación como función invertible aplicada a una key uniforme (semilla del **one-time pad**).

---

# Parte 2 — mml-book Cap 6 "Probability and Distributions" (6.1–6.2.1)

Source: *Mathematics for Machine Learning* (Deisenroth, Faisal, Ong, 2020) — [mml-book.github.io](https://mml-book.github.io/book/mml-book.pdf), Cap 6, p.152-180. TOC completo verificado contra el frontmatter oficial de Cambridge University Press (12 capítulos, no incluye cross-entropy ni softmax en ningún capítulo — ver `## Todavía falta` más abajo).

## 5. Construcción de un espacio de probabilidad (6.1)

**Random variable — el nombre es engañoso.** No es "aleatoria" ni "variable": es una **función** $X: \Omega \to \mathcal{T}$ que mapea un resultado de un experimento ($\Omega$, el *sample space*) a una cantidad de interés ($\mathcal{T}$, el *target space*). El libro lo marca explícito en un remark: el nombre es "a great source of misunderstanding".

**Los tres conceptos que arman un espacio de probabilidad:**
- **Sample space $\Omega$**: todos los resultados posibles del experimento. Ej. 2 tiradas de moneda → $\Omega = \{hh, tt, ht, th\}$.
- **Event space $\mathcal{A}$**: subconjuntos de $\Omega$ que se pueden observar (para casos discretos, el power set de $\Omega$).
- **Probability $P$**: número $P(A) \in [0,1]$ asociado a cada evento $A$, con $P(\Omega)=1$.

**Formalización con pre-imagen (Eq 6.8)** — conecta la probabilidad del *output* de X con la probabilidad de los *samples* que lo producen:
$$P_X(S) = P(X \in S) = P(X^{-1}(S)) = P(\{\omega \in \Omega : X(\omega) \in S\})$$
Esto es la versión formal de lo que ya vimos en Klein 0.4.3 (Parte 1 de esta nota, sección 3): "agrupar inputs que caen en el mismo output y sumar sus probs". Si $\mathcal{T}$ es finito/contable → discrete random variable; si $\mathcal{T} = \mathbb{R}$ o $\mathbb{R}^D$ → continuous random variable.

### Ejercicio — Example 6.1 (monedas $/£)

**Setup:** bolsa con monedas USA ($) y UK (£), se sacan 2 **con reemplazo** → tiradas independientes. Cada tirada da $ con prob 0.3 (→ £ con prob 0.7). Random variable $X$ = "cuántas veces salió $".

$$\Omega = \{(\$,\$),\ (\$,£),\ (£,\$),\ (£,£)\}, \quad X(\$,\$)=2,\ X(\$,£)=1,\ X(£,\$)=1,\ X(£,£)=0$$

**El punto clave:** dos outcomes distintos —$(\$,£)$ y $(£,\$)$— caen en el mismo valor $X=1$, por eso su probabilidad se **suma**, no es un solo caso:

$$P(X=2) = P(\$)\cdot P(\$) = 0.3 \cdot 0.3 = 0.09$$
$$P(X=1) = P(\$)\cdot P(£) + P(£)\cdot P(\$) = 0.3\cdot0.7 + 0.7\cdot0.3 = 0.42$$
$$P(X=0) = P(£)\cdot P(£) = 0.7\cdot0.7 = 0.49$$

Chequeo: $0.09+0.42+0.49=1$ ✓ — tiene que sumar 1, es la pmf completa de X.

**Contexto filosófico (6.1.1):** el libro justifica por qué probabilidad "generaliza" la lógica booleana clásica con el ejemplo del amigo que llega tarde (H1: a tiempo, H2: tráfico, H3: abducido por aliens) — lógica clásica no puede expresar "H2 se vuelve más plausible", probabilidad sí. Cox-Jaynes theorem: 3 criterios (números reales, sentido común, consistencia) son suficientes para derivar las reglas universales de la probabilidad. Dos interpretaciones conviven en ML: **Bayesiana** (grado de creencia subjetivo) vs **frecuentista** (frecuencia relativa en el límite de infinitos datos).

## 6. Probabilidad vs estadística (6.1.3)

Direcciones opuestas del mismo problema:
- **Probabilidad**: tenés el modelo (las random variables, las reglas) → derivás qué va a pasar.
- **Estadística**: viste qué pasó (los datos) → inferís qué modelo lo generó.

ML se parece a estadística en el objetivo (encontrar el modelo que mejor explica los datos que tenés) pero usa las reglas de probabilidad para lograrlo. Conecta con *generalization error* (Cap 8 del libro, todavía no cubierto): interesa la performance en instancias futuras no vistas, no solo en los datos ya observados.

## 7. Discrete vs continuous probabilities (6.2)

Dos formas de describir una distribución según el target space:
- **Discreto** → **pmf** (probability mass function): $P(X=x)$, probabilidad exacta de un valor puntual.
- **Continuo** → **cdf** (cumulative distribution function): $P(X \le x)$. En continuo $P(X = x \text{ exacto})$ da 0 (infinitos valores posibles), por eso tiene sentido acumular hasta un punto o pedir un intervalo $P(a \le X \le b)$.

**Univariate vs multivariate**: univariate = 1 sola random variable (estado $x$ minúscula, no-bold). Multivariate = varias random variables juntas, tratadas como vector (estado $\boldsymbol{x}$ bold). Ej: "altura de una persona" es univariate; "altura + peso + edad" es multivariate.

## 8. Joint, marginal y conditional probability (6.2.1)

**Joint probability** — probabilidad de que dos cosas pasen simultáneamente (intersección de eventos), visualizada como grilla (Fig 6.2: X en columnas, Y en filas, cada celda $n_{ij}$ = conteo de esa combinación exacta):
$$P(X=x_i, Y=y_j) = \frac{n_{ij}}{N} = P(X=x_i \cap Y=y_j)$$

### Ejercicio — Example 6.2

Mismo grid: X con 5 estados, Y con 3 estados, $N$ = total de eventos.

**Marginal** = "me olvido de la otra variable, solo me importa esta" — sumás toda una fila o columna:
$$P(X=x_i) = \frac{c_i}{N} = \frac{\sum_{j=1}^{3} n_{ij}}{N} \qquad P(Y=y_j) = \frac{r_j}{N} = \frac{\sum_{i=1}^{5} n_{ij}}{N}$$
donde $c_i$ = suma de columna $i$, $r_j$ = suma de fila $j$. Por convención $\sum_i P(X=x_i)=1$ y $\sum_j P(Y=y_j)=1$. Se llama "marginal" literal porque es la suma en el margen de la tabla.

**Conditional** = "dado que ya sé el valor de una, qué fracción de ESOS casos tiene el otro valor" — no divide por $N$ total, divide por el subtotal de esa fila/columna:
$$P(Y=y_j \mid X=x_i) = \frac{n_{ij}}{c_i} \qquad P(X=x_i \mid Y=y_j) = \frac{n_{ij}}{r_j}$$

**Diferencia clave marginal vs conditional:** marginal divide por $N$ (población total), conditional divide por el subtotal de la condición (población ya filtrada) — achicás el universo antes de calcular la fracción.

**Aplicación ML:** distribuciones discretas modelan **categorical variables** — features categóricas (ej. carrera universitaria para predecir salario) o labels categóricas (ej. letras del alfabeto en reconocimiento de escritura). También se usan para construir modelos que combinan un número finito de distribuciones continuas (Cap 11, Gaussian Mixture Models — ver Fig 6.1 mind map, Parte 2 sección 5).

---

## Para developer — resumen

- Distribución de prob = dict que suma 1.
- Evento = subconjunto de outcomes → sumás sus probabilidades.
- Aplicar función a variable aleatoria = "reduce por output" (agrupar inputs que caen en el mismo output y sumar sus probs).
- Función invertible + input uniforme → output uniforme. Esta es la base matemática de por qué XOR con una key random (one-time pad) es indetectable.
- Random variable = función (no es "aleatoria" ni "variable"), $X: \Omega \to \mathcal{T}$.
- pmf (discreto) vs cdf (continuo); joint (intersección) vs marginal (sumás la otra variable, dividís por N total) vs conditional (dividís por el subtotal de la condición, no por N total).

## Repaso 2026-08-14 — framing 100% dev

Sesión anterior no quedó clara (mucha notación densa de golpe). Reconstruido con analogías 100% dev, sin tocar contenido nuevo:

- **Distribución** = un dict que suma 1: `Pr = {'heads': 0.5, 'tails': 0.5}`.
- **Random variable** = una función pura `def X(outcome): ...`, no es "aleatoria" — lo aleatorio es el input, no la función.
- **Aplicar función a input random** = `GROUP BY output + SUM(prob)`. Código: `out[f(outcome)] += p` por cada `(outcome, p)`.
- **Función invertible + input uniforme → output uniforme**: sin collisions en el groupby, cada output tiene un único input. Base del one-time pad.
- **pmf vs cdf**: pmf = lookup exacto `dict[x]` (discreto). cdf = query acumulado `WHERE x <= 5` (continuo, porque un punto exacto tiene masa cero).
- **Marginal vs conditional** = dos queries sobre la misma tabla de counts: marginal divide por N total (`count(X==x1)/total_rows`), conditional divide por el subtotal ya filtrado (`count(X==x1 and Y==y1)/count(X==x1)`) — el denominador cambia porque ya restringiste el universo.

Confidence subió 2/5 → 3/5: el modelo mental ahora es sólido, pero **expectation/mean/variance/covariance (6.4) sigue siendo el gap real** — ahí es donde sigue el roadmap.

## Todavía falta (roadmap Phase 0)

- **Continuous probabilities (mml-book 6.2.2)** — quedó pendiente, es lo próximo a retomar en Cap 6.
- **Sum Rule, Product Rule, Bayes' Theorem (6.3)** — no cubierto todavía.
- **Expectation, mean, variance, covariance (6.4 "Summary Statistics and Independence")** — esto es lo que resuelve el gap de "expectation" del roadmap; vive en esta sección, no en 6.1-6.2.
- **Gaussian distribution (6.5)** — no cubierto todavía.
- **Cross-entropy y softmax** — CONFIRMADO ausente de mml-book (TOC completo de los 12 capítulos verificado contra el frontmatter oficial de Cambridge, 2026-08-11 — el libro cubre solo 4 métodos: regresión lineal, PCA, GMM, SVM, ninguno usa softmax/cross-entropy como loss). Necesita fuente aparte: Raschka *Build a LLM from Scratch* (ya en el roadmap Phase 2), CS231n notes (softmax classifier), o 3Blue1Brown "But what is a neural network" ep.3.

**Prioridad:** gap más grande de Phase 0 (2/5, vs. álgebra lineal en 5/5) — seguir con 6.2.2 → 6.3 → 6.4 (expectation) antes de arrancar Phase 1 (la loss de un clasificador usa cross-entropy directo, que va a necesitar la fuente externa arriba).

## Ver también

- [[Coding-the-Matrix-Fundamentals]] — funciones, invertibilidad (prerequisito de esta nota)
