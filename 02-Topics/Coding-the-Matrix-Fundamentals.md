---
tags: [phase-0, math, linear-algebra, coding-the-matrix]
status: learning
first_learned: 2026-07-01
last_reviewed: 2026-07-01
confidence: 2/5
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Coding the Matrix — Fundamentos (Klein)

Source: *Coding the Matrix: Linear Algebra through Computer Science Applications* (1st ed.), Philip N. Klein — PDF en `00-Meta/resources/Philip N. Klein-Coding the Matrix...pdf`

## 1. Cartesian product y cardinalidad (Cap 0.2, p.2)

**Idea simple:** el producto cartesiano $A \times B$ es el conjunto de TODOS los pares posibles combinando un elemento de A con uno de B. Pensalo como nested loop: por cada elemento de A, generás un par nuevo con cada elemento de B.

```
for a in A:
    for b in B:
        yield (a, b)
```

Total de pares generados = (cantidad de iteraciones del loop externo) × (cantidad de iteraciones del loop interno) = $|A| \times |B|$.

**Fórmula (Proposition 0.2.3, p.2):**
$$|A \times B| = |A| \cdot |B|$$

**Ejemplo verificado (Example 0.2.1 / Quiz 0.2.2, p.2):** $A=\{1,2,3\}$ ($|A|=3$), $B=\{\heartsuit,\spadesuit,\clubsuit,\diamondsuit\}$ ($|B|=4$) → $|A \times B| = 3 \times 4 = 12$ pares, coincide con la lista completa del ejemplo.

---

## 2. La función (Cap 0.3, p.2-3)

**Idea simple:** una función matemática es literalmente un **dict/hashmap** — cada input (key) mapea a exactamente un output (value), nunca a dos valores distintos. "Dominio" = el conjunto de keys válidas. "Imagen" (de un input específico) = el value que le corresponde. "Pre-imagen" = la key que produjo ese value.

**Definición formal (p.2-3):** una función es un conjunto de pares $(a,b)$ donde ningún par comparte la misma primera entrada (ningún key duplicado — si tuvieras dos pares con el mismo `a` pero distinto `b`, no sería función, sería ambigua).

$$f = \{(a,b) : \text{ningún par comparte la misma primera entrada } a\}$$

- **Dominio ($D$):** conjunto de todos los inputs posibles (todos los `a`).
- **Imagen de un input:** el output que le corresponde (`b`).
- **Pre-imagen de un output:** el input que lo produjo (`a`).

### Ejemplos citados

**Example 0.3.1 (p.2) — función de duplicar:** dominio $\{1,2,3,...\}$, función = $\{(1,2),(2,4),(3,6),(4,8),...\}$. Como código: `{n: 2*n for n in range(1, N)}`.

**Example 0.3.2 (p.2) — multiplicación:** el dominio puede ser en sí un producto cartesiano — acá dominio = $\{1,2,3,...\} \times \{1,2,3,...\}$ (pares de números), función = $\{((1,1),1),((1,2),2),((2,2),4),((2,3),6),...\}$. Osea: el input mismo es una tupla `(a,b)`, el output es `a*b`.

**Example 0.3.3 (p.3) — cifrado César:** cada letra se reemplaza por la que está 3 posiciones adelante en el alfabeto (con wraparound pa X,Y,Z). Dominio y codominio son el mismo conjunto: el alfabeto $\{A,B,...,Z\}$.

$$A \mapsto D,\ B \mapsto E,\ C \mapsto F,\ \ldots,\ X \mapsto A,\ Y \mapsto B,\ Z \mapsto C$$

`MATRIX` se encripta como `PDWULA` (cada letra +3, con wraparound). En código: literal un dict de 26 entradas, o `chr((ord(c)-65+3)%26+65)`.

**Por qué importa:** este ejemplo (dominio=codominio, cada input mapea a exactamente un output, y la función es invertible — se puede desencriptar restando 3) es la semilla de "función invertible" que después se conecta con **matriz invertible** en Cap 4 — misma idea, escalada a vectores.

---

## 3. Notación $F^D$ y función identidad (Cap 0.3.3-0.3.4, p.6)

**Idea simple:** $F^D$ no es una función — es el conjunto de TODAS las funciones posibles con dominio D y codominio F. Como pensar en todos los programas posibles con una firma de tipo dada, no un programa en particular.

**Por qué el exponente (Fact 0.3.9, p.6):** cada elemento del dominio elige independientemente uno de los valores del codominio. Multiplicás las opciones una vez por cada input:

$$|D^F| = |D|^{|F|}$$

Ejemplo: dominio 3 elementos, codominio 2 elementos → $2^3=8$ funciones distintas posibles (como contar combinaciones de bits, o dicts posibles con 3 keys fijas y values booleanos).

**Función identidad (p.6):** devuelve exactamente el input, sin modificarlo — el "no-op" de las funciones.

$$\text{id}_D(d) = d \quad \text{para todo } d \in D$$

En código: `lambda x: x`. Es el elemento neutro al componer funciones (igual rol que la matriz identidad $I$ en Cap 4 — multiplicar por $I$ no cambia nada).

---

## 4. Inverso funcional (Cap 0.3.7, p.7-8)

**Idea simple:** el inverso de una función "deshace" su efecto. Si `f` te lleva de A a B, su inverso `g` te trae de vuelta de B a A. Aplicar una y después la otra (en cualquier orden) = no-op, quedás donde empezaste.

**Ejemplo del cifrado César:** `f` = encriptar (+3 con wraparound). Su inverso `g` = desencriptar (-3 con wraparound). `encrypt(decrypt(x)) == x` y `decrypt(encrypt(x)) == x` pa todo x.

**Definición formal (0.3.13, p.7):** $f$ y $g$ son inversos funcionales si se cumplen LAS DOS condiciones (no alcanza con una sola dirección):

$$f \circ g = \text{id}_{\text{dominio de } g}$$
$$g \circ f = \text{id}_{\text{dominio de } f}$$

**No toda función es invertible.** Falla cuando dos inputs distintos mapean al mismo output (ej. $f(1)=5$ y $f(2)=5$) — el inverso no sabría si devolver 1 o 2 al ver un 5, hay ambigüedad. Función con inverso = *invertible*.

**Por qué importa:** esta idea exacta (invertibilidad, deshacer sin ambigüedad) se escala a matrices en Cap 4 — matriz invertible = misma lógica pero para transformaciones lineales completas, no solo funciones sobre un elemento.

---

## Ver también

- [[Linear-Algebra-Axler-Fundamentals]] — versión formal/rigurosa (Axler)
- [[Linear-Algebra-Basics]] — intuición geométrica (3b1b)
