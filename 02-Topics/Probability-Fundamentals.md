---
tags: [phase-0, math, probability, coding-the-matrix, mml-book]
status: learning
first_learned: 2026-07-01
last_reviewed: 2026-08-16
confidence: 4/5
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

## 9. Continuous probabilities — pdf y cdf (6.2.2–6.2.3)

**pdf (probability density function)** — Definition 6.1: $f:\mathbb{R}^D\to\mathbb{R}$ es pdf si (1) $f(\boldsymbol{x})\geq 0$ para todo $\boldsymbol{x}$, (2) $\int_{\mathbb{R}^D} f(\boldsymbol{x})\,d\boldsymbol{x}=1$. Se asocia a una random variable $X$ vía $P(a\leq X\leq b)=\int_a^b f(x)\,dx$ (Eq 6.16) — esta asociación se llama **law** o **distribution** de $X$.

**Diferencia clave con pmf:** en discreto, la altura de la barra ES la probabilidad. En continuo, la altura del pdf es **densidad**, NO probabilidad — puede pasar de 1 (Table 6.1 lo remarca explícito, imagen 7 de la sesión). Para sacar probabilidad real en continuo hace falta integrar (área), nunca leer un punto — por eso $P(X=x\text{ exacto})=0$ en continuo.

**cdf (cumulative distribution function)** — Definition 6.2: $F_X(\boldsymbol{x})=P(X_1\leq x_1,\ldots,X_D\leq x_D)$ (Eq 6.17), o como integral del pdf: $F_X(\boldsymbol{x})=\int_{-\infty}^{x_1}\cdots\int_{-\infty}^{x_D} f(z_1,\ldots,z_D)\,dz_1\cdots dz_D$ (Eq 6.18).

**Tabla de nomenclatura (Table 6.1):**

| | Point probability | Interval probability |
|---|---|---|
| Discrete | $P(X=x)$ — pmf | no aplica |
| Continuous | $p(x)$ — pdf | $P(X\leq x)$ — cdf |

**Example 6.3** (uniforme discreta vs continua, Figure 6.3): $Z$ discreta uniforme en 3 estados $\{-1.1, 0.3, 1.5\}$, cada uno con $P(Z=z)=1/3$ (altura = prob real). $X$ continua uniforme en $[0.9, 1.6)$, con densidad constante $p(x)\approx 1.43$ (altura = $1/\text{ancho}$, para que $\int_{0.9}^{1.6}p(x)\,dx=1$, Eq 6.19) — la densidad supera 1 sin violar ninguna regla, porque lo que tiene que sumar 1 es el ÁREA, no la altura.

**Aplicación dev:** softmax de un clasificador es literal un pmf (lookup exacto). Percentiles de latencia (p50, p99) son literal un cdf invertido. Una Gaussiana sobre residuos de un modelo es un pdf.

## 10. Sum Rule, Product Rule y Bayes' Theorem (6.3)

Solo 2 reglas fundamentales, de las que se deriva todo lo demás (Jaynes 2003).

**Sum Rule (marginalization)** — Eq 6.20: $p(\boldsymbol{x})=\sum_{\boldsymbol{y}\in\mathcal{Y}} p(\boldsymbol{x},\boldsymbol{y})$ (discreto) o la integral equivalente (continuo). Es literal la **marginal** ya vista en sección 8 — "sumar/integrar afuera" la otra variable. Generaliza a más variables (Eq 6.21). *Remark:* esta suma/integral de alta dimensión es la fuente de la mayoría de los desafíos computacionales de probabilistic modeling — no hay algoritmo polinomial exacto en general.

**Product Rule (factorización)** — Eq 6.22: $p(\boldsymbol{x},\boldsymbol{y})=p(\boldsymbol{y}\mid\boldsymbol{x})\,p(\boldsymbol{x}) = p(\boldsymbol{x}\mid\boldsymbol{y})\,p(\boldsymbol{y})$. Toda joint se puede factorizar como marginal × conditional. Base de **Naive Bayes**: $p(\text{clase},\text{features})=p(\text{features}\mid\text{clase})\,p(\text{clase})$.

**Bayes' Theorem** — Eq 6.23, consecuencia directa de igualar las 2 factorizaciones del product rule:

$$\underbrace{p(\boldsymbol{x}\mid\boldsymbol{y})}_{\text{posterior}}=\dfrac{\overbrace{p(\boldsymbol{y}\mid\boldsymbol{x})}^{\text{likelihood}}\ \overbrace{p(\boldsymbol{x})}^{\text{prior}}}{\underbrace{p(\boldsymbol{y})}_{\text{evidence}}}$$

- **Prior** $p(\boldsymbol{x})$: creencia previa sobre la variable latente $\boldsymbol{x}$, antes de ver datos. Debe tener pdf/pmf $\neq 0$ en todo lo plausible.
- **Likelihood** $p(\boldsymbol{y}\mid\boldsymbol{x})$: NO es distribución en $\boldsymbol{x}$, solo en $\boldsymbol{y}$ — "prob de los datos si supiéramos $\boldsymbol{x}$". Se dice "likelihood de $\boldsymbol{x}$ dado $\boldsymbol{y}$", nunca "likelihood de $\boldsymbol{y}$" (MacKay 2003).
- **Evidence/marginal likelihood** $p(\boldsymbol{y}):=\int p(\boldsymbol{y}\mid\boldsymbol{x})p(\boldsymbol{x})\,d\boldsymbol{x}=\mathbb{E}_X[p(\boldsymbol{y}\mid\boldsymbol{x})]$ (Eq 6.27) — es literal sum rule aplicado al numerador, normaliza el posterior.
- **Posterior** $p(\boldsymbol{x}\mid\boldsymbol{y})$: lo que interesa en Bayesian stats — qué sé de $\boldsymbol{x}$ después de observar $\boldsymbol{y}$. Se llama también "probabilistic inverse" — invierte la relación que da la likelihood.

Visual (fórmula completa con etiquetas): [[07-Visuals/bayes-theorem-2026-08-16.html]]

**Ejercicio resuelto en sesión — filtro de spam:** $x$=es spam (latente), $y$=contiene "gratis" (observado). Prior $P(\text{spam})=0.20$. Likelihood $P(\text{"gratis"}\mid\text{spam})=0.50$, $P(\text{"gratis"}\mid\text{no\_spam})=0.05$. Evidence $=0.50\cdot0.20+0.05\cdot0.80=0.14$. Posterior $=(0.50\cdot0.20)/0.14=0.714$ — la creencia de spam saltó de 20% a 71.4% con un solo dato.

## 11. Expected value, mean, median, mode (6.4.1 parte 1)

**Expected value** — Definition 6.3: $\mathbb{E}_X[g(x)]=\int_{\mathcal{X}} g(x)p(x)\,dx$ (continuo, Eq 6.28) o $\sum_{x\in\mathcal{X}} g(x)p(x)$ (discreto, Eq 6.29) — promedio ponderado por probabilidad de $g(x)$, para cualquier función $g$. Para multivariate, se define elemento a elemento (Eq 6.30).

**Mean** — Definition 6.4: caso especial con $g=$identidad. $\mathbb{E}_X[\boldsymbol{x}]$ (Eq 6.31). Diferencia con "promedio simple": pesa cada valor por su probabilidad, no por 1/N — solo coinciden si la distribución es uniforme.

**Median**: valor donde cdf$=0.5$ (50% arriba, 50% abajo) — más robusto a outliers/asimetría que la media. **Mode**: valor más frecuente (pico de la pmf/pdf) — puede haber múltiples modes.

**Example 6.4** (Figure 6.4, mixture bimodal 2D): mean y median pueden diferir en distribuciones asimétricas/multimodales — la mediana 2D no se puede definir trivialmente concatenando medianas por eje porque no hay orden natural en $\mathbb{R}^2$.

**Linealidad del expected value** (Eq 6.34): $\mathbb{E}_X[a\,g(x)+b\,h(x)]=a\,\mathbb{E}_X[g(x)]+b\,\mathbb{E}_X[h(x)]$.

## 12. Covariance, variance, covariance matrix, correlation (6.4.1 parte 2)

**Covariance** — Definition 6.5: $\mathrm{Cov}[x,y]:=\mathbb{E}[(x-\mathbb{E}[x])(y-\mathbb{E}[y])]$ (Eq 6.35), reescrita por linealidad como **raw-score formula**: $\mathrm{Cov}[x,y]=\mathbb{E}[xy]-\mathbb{E}[x]\mathbb{E}[y]$ (Eq 6.36) — la versión que se usa para calcular en la práctica.

**Variance = covarianza de una variable consigo misma**: $\mathbb{V}[x]=\mathrm{Cov}[x,x]$. $\sigma(x)=\sqrt{\mathbb{V}[x]}$ = standard deviation.

**Covariance matrix** (multivariate, Definition 6.6-6.7): matriz $D\times D$ con $\mathrm{Cov}[x_i,x_j]$ en cada celda $(i,j)$ — diagonal = varianzas individuales, fuera de diagonal = cross-covariance. Simétrica, positive semidefinite. Base matemática de PCA.

**Correlation** — Definition 6.8: $\mathrm{corr}[x,y]=\dfrac{\mathrm{Cov}[x,y]}{\sqrt{\mathbb{V}[x]\mathbb{V}[y]}}\in[-1,1]$ — covarianza normalizada por las escalas de cada variable (Figure 6.5: mismas varianzas por eje, distinta covarianza → nubes con distinta inclinación).

**Ejercicio resuelto — tabla de logs (X=método{GET=0,POST=1}, Y=status{200=0,404=1}):** $\mathrm{Cov}[X,Y]=P(\text{POST},404)-P(\text{POST})P(404)=0.15-0.10=0.05$. $\mathbb{V}[X]=0.24$, $\mathbb{V}[Y]=0.1875$. $\mathrm{corr}[X,Y]=0.05/\sqrt{0.24\cdot0.1875}=0.2357$ — correlación positiva moderada: ser POST está asociado con más 404.

## 13. Empirical mean/covariance (6.4.2)

Lo de la sección 11-12 es **population** mean/covariance (estadística real, teórica). En ML se aprende de un dataset finito de $N$ observaciones — se usa la versión **empirical/sample**:

$$\bar{\boldsymbol{x}}:=\frac{1}{N}\sum_{n=1}^N \boldsymbol{x}_n \quad\text{(Eq 6.41)} \qquad \boldsymbol{\Sigma}:=\frac{1}{N}\sum_{n=1}^N(\boldsymbol{x}_n-\bar{\boldsymbol{x}})(\boldsymbol{x}_n-\bar{\boldsymbol{x}})^\top \quad\text{(Eq 6.42)}$$

Literal `np.mean(X, axis=0)` y `np.cov(X.T)`. El libro usa la versión "biased" (divide por $N$); la "unbiased/corrected" divide por $N-1$.

**Gotcha verificado en review 2026-08-16:** `np.cov(X.T)` por default usa `ddof=1` (N-1, "unbiased") — NO reproduce Eq 6.42 tal cual está escrita en el libro (que divide por N). Para replicar Eq 6.42 exacto: `np.cov(X.T, ddof=0)` o `bias=True`.

## 14. Tres expresiones de la varianza (6.4.3)

1. **Definición estándar** (Eq 6.43): $\mathbb{V}_X[x]:=\mathbb{E}_X[(x-\mu)^2]$ — requiere 2 pasadas por los datos (mean primero, luego varianza con esa mean).
2. **Raw-score formula** (Eq 6.44): $\mathbb{V}_X[x]=\mathbb{E}_X[x^2]-(\mathbb{E}_X[x])^2$ — "mean del cuadrado menos cuadrado de la mean", permite 1 sola pasada (acumular $x$ y $x^2$ juntos), aunque puede ser numéricamente inestable si ambos términos son grandes y casi iguales.
3. **Pairwise differences** (Eq 6.45): $\frac{1}{N^2}\sum_{i,j}(x_i-x_j)^2 = 2\times$ raw-score — equivale matemáticamente pero es $O(N^2)$ en vez de $O(N)$, por eso nunca se usa en código.

## 15. Sums y transformaciones afines de random variables (6.4.4)

Para $X,Y$ con estados en $\mathbb{R}^D$:

$$\mathbb{E}[x+y]=\mathbb{E}[x]+\mathbb{E}[y] \quad(6.46) \qquad \mathbb{V}[x+y]=\mathbb{V}[x]+\mathbb{V}[y]+2\,\mathrm{Cov}[x,y] \quad(6.48)$$

La covarianza SÍ importa en la varianza de la suma: si están correlacionadas positivamente, $\mathbb{V}[x+y]$ es mayor que la suma de varianzas por separado.

**Transformación afín** $\boldsymbol{y}=\boldsymbol{A}\boldsymbol{x}+\boldsymbol{b}$ (una capa lineal sin activación) de $X$ con media $\mu$, covarianza $\Sigma$:

$$\mathbb{E}_Y[\boldsymbol{y}]=\boldsymbol{A}\mu+\boldsymbol{b} \quad(6.50) \qquad \mathbb{V}_Y[\boldsymbol{y}]=\boldsymbol{A}\Sigma\boldsymbol{A}^\top \quad(6.51)$$

Base matemática de por qué una capa lineal transforma la distribución de sus inputs de forma predecible — relevante para entender batch normalization más adelante.

## 16. Statistical independence, i.i.d., conditional independence (6.4.5)

**Independence** — Definition 6.10: $X\perp Y \iff p(\boldsymbol{x},\boldsymbol{y})=p(\boldsymbol{x})p(\boldsymbol{y})$ (Eq 6.53). Si independientes: $p(y\mid x)=p(y)$, $\mathbb{V}[x+y]=\mathbb{V}[x]+\mathbb{V}[y]$, $\mathrm{Cov}[x,y]=0$.

**El recíproco NO vale** — covarianza 0 no implica independencia, porque covarianza solo mide dependencia LINEAL. Example 6.5: $X$ con media 0 y $\mathbb{E}[x^3]=0$, $Y=x^2$ (dependiente de $X$ no-linealmente) → $\mathrm{Cov}[x,y]=\mathbb{E}[x^3]=0$ (Eq 6.54) pese a dependencia clara.

**Ejercicio resuelto — tabla de logs:** $P(\text{GET},200)=0.50$ vs $P(\text{GET})\cdot P(200)=0.60\cdot0.75=0.45$ — no coinciden → GET/status NO son independientes (coherente con correlación $\neq 0$ del ejercicio anterior).

**i.i.d.** (independent and identically distributed): supuesto base de casi todo ML — samples independientes entre sí ("independent") Y todos vienen de la misma distribución ("identically distributed").

**Conditional independence** — Definition 6.11: $X\perp Y\mid Z \iff p(\boldsymbol{x},\boldsymbol{y}\mid \boldsymbol{z})=p(\boldsymbol{x}\mid\boldsymbol{z})\,p(\boldsymbol{y}\mid\boldsymbol{z})$ para todo $z$ (Eq 6.55) — "dado que sé $z$, saber $y$ no cambia mi conocimiento de $x$" (forma alternativa Eq 6.57: $p(x\mid y,z)=p(x\mid z)$). Base de Naive Bayes y de Bayesian networks.

## 17. Inner products de random variables — correlación como coseno (6.4.6)

Random variables se pueden tratar como vectores en un espacio vectorial abstracto, con $\langle X,Y\rangle:=\mathrm{Cov}[x,y]$ (Eq 6.59, para variables de media cero) — cumple las propiedades de un inner product real (simétrico, positive definite, lineal).

- **Norma** = $\|X\|=\sqrt{\mathrm{Cov}[x,x]}=\sqrt{\mathbb{V}[x]}=\sigma[x]$ (Eq 6.60) — la standard deviation ES la norma en este espacio.
- **Ángulo**: $\cos\theta=\dfrac{\langle X,Y\rangle}{\|X\|\|Y\|}=\dfrac{\mathrm{Cov}[x,y]}{\sqrt{\mathbb{V}[x]\mathbb{V}[y]}}$ (Eq 6.61) — **esto ES la correlación**: la correlación es el coseno del ángulo entre 2 variables vistas como vectores.
- **Ortogonalidad**: $X\perp Y \iff \mathrm{Cov}[x,y]=0$ (no correlacionadas = perpendiculares).
- **Pitágoras** (Figure 6.6): si no correlacionadas, $\mathbb{V}[x+y]=\mathbb{V}[x]+\mathbb{V}[y]$ (Eq 6.58) — literal $c^2=a^2+b^2$ con $\sqrt{\mathbb{V}}$ como catetos/hipotenusa.

Conecta directo con [[Coding-the-Matrix-Fundamentals]] — mismo inner product/norma/ángulo/ortogonalidad de vectores geométricos, aplicado a un espacio abstracto donde el "producto punto" es la covarianza.

---

## Ejercicios de sesión 2026-08-16 (dado cargado, tabla de logs, numpy)

- **Dado cargado** (P(6)=0.5, resto 0.1 c/u): $\mathbb{E}[X]=4.5$, $\mathbb{V}[X]=\mathbb{E}[X^2]-(\mathbb{E}[X])^2=23.5-20.25=3.25$.
- **Tabla de logs** (GET/POST × 200/404): covarianza, correlación e independencia resueltos en secciones 12 y 16 arriba.
- **numpy** (`np.cov`, `np.corrcoef` con 20 puntos $y\approx 2x+\text{ruido}$): confirmó estructura de matriz cov/corr — correlación 0.96 (relación lineal fuerte a propósito). Ver script generado en sesión.

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

- **Gaussian distribution (6.5)** — no cubierto todavía, es lo próximo a retomar en Cap 6. `probability_distributions_expectation` (gap del roadmap) queda RESUELTO con la sesión 2026-08-16 (6.2.2–6.4 completos, ver secciones 9-17 arriba).
- **6.6 (Conjugacy/Exponential Family) y 6.7 (Change of Variables)** — verificado 2026-08-16 vía TOC oficial de Cambridge: NO son parte del roadmap actual (relevantes solo para Bayesian deep learning / normalizing flows, fuera de scope de Phase 0-7). 6.8 es solo "Further Reading", no tiene contenido.
- **Cross-entropy y softmax** — CONFIRMADO ausente de mml-book (TOC completo de los 12 capítulos verificado contra el frontmatter oficial de Cambridge, 2026-08-11 — el libro cubre solo 4 métodos: regresión lineal, PCA, GMM, SVM, ninguno usa softmax/cross-entropy como loss). Necesita fuente aparte: Raschka *Build a LLM from Scratch* (ya en el roadmap Phase 2), CS231n notes (softmax classifier), o 3Blue1Brown "But what is a neural network" ep.3.

**Prioridad:** gap más grande de Phase 0 (2/5, vs. álgebra lineal en 5/5) — seguir con 6.2.2 → 6.3 → 6.4 (expectation) antes de arrancar Phase 1 (la loss de un clasificador usa cross-entropy directo, que va a necesitar la fuente externa arriba).

## 18. Bayes visual — 3Blue1Brown "Essence of probability" (Kahneman & Tversky)

Complemento del libro con la serie de YouTube [3Blue1Brown — Essence of probability](https://www.youtube.com/playlist?list=PLiAulSm0XXgvCGe63mrAkda9UQ9478YQv), video "Bayes' theorem".

**Cuadrado unitario (1x1) como intuición geométrica de Bayes:** en vez de memorizar la fórmula, dibujar un cuadrado de área 1 (población normalizada). Una franja de ancho $P(H)$ representa la hipótesis; dentro de ella, la porción $P(E|H)$ representa "de los H, cuántos encajan con la evidencia"; fuera, $P(E|\neg H)$ representa lo mismo para $\neg H$. $P(H|E)$ es la fracción de TODA el área-que-encaja-con-E que además es H.

**Lo crucial es la asimetría entre $P(E|H)$ y $P(E|\neg H)$** (likelihood ratio): si ambas franjas tuvieran la misma altura, ver la evidencia no movería la creencia en absoluto ($P(H|E)=P(H)$). Cuanto mayor la diferencia entre esas 2 alturas, más fuerte "empuja" la evidencia el update — es el motor real detrás de Bayes, y la misma idea detrás de model selection Bayesiano (comparar qué tan bien cada modelo explica los datos observados vía su likelihood).

### Caso Steve — base-rate neglect (Tversky & Kahneman, *Science* 1974)

Experimento: descripción de personalidad de "Steve" (tímido, ordenado, meticuloso) → ¿es más probable que sea bibliotecario o granjero? La mayoría vota 81% granjero / 19% bibliotecario basándose SOLO en la descripción — el estudio real es 40% de bibliotecarios encajan con la descripción vs 10% de granjeros, PERO hay ~20x más granjeros que bibliotecarios en la población, así que aplicando Bayes con prior $P(H)=1/21$: $P(bibliotecario|descripción) = 4/(4+20) \approx 16.7\%$ — la gente ignora el prior (proporción poblacional) y confía solo en el likelihood. Este es el sesgo llamado **representativeness heuristic**, que produce **base-rate neglect**: juzgar probabilidad por cuánto se parece algo al estereotipo, ignorando la frecuencia real de esa categoría.

### Caso Linda — conjunction fallacy (mismo par de autores, "Linda problem")

Descripción de "Linda" (filósofa, activista) → ¿es más probable que sea (1) cajera de banco, o (2) cajera de banco Y activista feminista? 85% de los participantes eligió (2), pese a ser matemáticamente imposible: "cajeras feministas" es un SUBCONJUNTO de "cajeras", por lo que $P(A \cap B) \leq P(A)$ siempre. Mismo mecanismo (representativeness): la conjunción "suena" más representativa de Linda aunque sea menos probable.

**Crítica de Gigerenzer (verificada vía web, 2026-08-16):** Gerd Gigerenzer mostró que reformulando la pregunta como frecuencia concreta ("de 100 personas que encajan con la descripción, ¿cuántas son cajeras? ¿cuántas son cajeras-y-feministas?") en vez de probabilidad abstracta, el error de conjunción CAE fuerte (de >80% a 20-40%) — su argumento es que el cerebro razona mejor con conteos de frecuencia que con probabilidades condicionales abstractas. Kahneman/Tversky respondieron que ya habían documentado ese efecto de frecuencia ellos mismos. Estudios posteriores confirman: el sesgo BAJA con framing de frecuencia pero no desaparece del todo (sigue habiendo 20-40% de error) — Gigerenzer no refuta la matemática de Bayes, cuestiona qué tan bien razona la mente humana con ella sin ayuda visual.

**Conclusión del video, útil para el resto del path:** probabilidad es la matemática de las proporciones — Bayes visto como áreas/proporciones muestra literalmente "qué fracción de los casos-que-encajan-con-la-evidencia corresponden a la hipótesis". No hace falta memorizar la fórmula si podés dibujar el cuadrado cuando lo necesites.

**Lectura recomendada (verificada, no de memoria):** Daniel Kahneman — *Thinking, Fast and Slow* (2011), la puerta de entrada accesible a este trabajo (Tversky murió en 1996, no pudo compartir el Nobel de Economía 2002 que Kahneman ganó por esta investigación). El paper académico original, "Judgment under Uncertainty: Heuristics and Biases" (*Science*, 1974), es corto y gratuito.

## Ver también

- [[Coding-the-Matrix-Fundamentals]] — funciones, invertibilidad (prerequisito de esta nota)
