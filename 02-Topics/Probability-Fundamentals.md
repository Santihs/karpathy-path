---
tags: [phase-0, math, probability, coding-the-matrix]
status: seed
first_learned: 2026-07-01
last_reviewed: 2026-07-01
confidence: 1/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
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

## Para developer — resumen

- Distribución de prob = dict que suma 1.
- Evento = subconjunto de outcomes → sumás sus probabilidades.
- Aplicar función a variable aleatoria = "reduce por output" (agrupar inputs que caen en el mismo output y sumar sus probs).
- Función invertible + input uniforme → output uniforme. Esta es la base matemática de por qué XOR con una key random (one-time pad) es indetectable.

## Todavía falta (roadmap Phase 0)

- **Expectation (valor esperado)** — no cubierto en este capítulo de Klein.
- **Cross-entropy y softmax** — necesita sesión aparte, conecta directo con loss functions de ML (fuera de scope de Klein Cap 0).

## Ver también

- [[Coding-the-Matrix-Fundamentals]] — funciones, invertibilidad (prerequisito de esta nota)
