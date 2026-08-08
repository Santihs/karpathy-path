---
tags: [phase-0, coding-the-matrix, machine-learning, gradient-descent, optimization, history]
date_resolved: 2026-08-08
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# De dónde viene gradient descent — no fue inventado para IA

**Duda:** ¿cómo llegaron los AI engineers a esta conclusión (gradient descent)? Quería el porqué conceptual, no solo las fórmulas.

## No es un invento de machine learning

Augustin-Louis Cauchy, matemático francés, formuló el método en **1847** para resolver ecuaciones no-lineales generales — sin ninguna relación con IA ni con "entrenar modelos". Su observación central: una función continua tiene que bajar de valor si te movés en la dirección opuesta a su pendiente local. Es la formalización de algo casi intuitivo — una pelota rodando cuesta abajo sigue la inclinación local del terreno bajo sus pies, sin ver el mapa completo.

## Atribución histórica enredada

A veces se le atribuye al físico Peter Debye (1909, en un estudio asintótico de funciones de Bessel), aunque el propio Debye dijo que la tomó de un paper de Bernhard Riemann de 1863. El matemático ruso Pavel Nekrasov ya la había usado y generalizado 25 años antes que Debye. Kantorovitch (1945) la formuló en la versión moderna para sistemas lineales con matrices simétricas positivas definidas.

## Por qué hace falta recalcular en cada paso

En una función LINEAL, la pendiente es la misma en todos lados — se calcula la dirección de bajada una sola vez. Pero en una función no-lineal (como `L(w)`, que es cuadrática), la pendiente cambia según dónde estás parado — por eso gradient descent es un algoritmo *iterativo*, no una fórmula de un solo paso: hay que recalcular el gradiente después de cada movimiento.

## Por qué terminó siendo el algoritmo de entrenamiento de IA

No fue diseñado para redes neuronales — se aplicó porque "entrenar un modelo" resultó ser matemáticamente idéntico al problema de Cauchy: hay una función (la loss) que depende de muchos parámetros, y hace falta encontrar los valores que la minimizan. Nadie sabe resolver esto algebraicamente para funciones complicadas (redes con millones de parámetros), pero sí se puede calcular la pendiente local en cualquier punto — literalmente lo que hace `loss.backward()` en PyTorch, automatizando el cálculo de derivadas parciales vía autograd (grafo de cómputo + regla de la cadena aplicada en reversa), en vez de que alguien derive la fórmula a mano como se hizo en este lab con `find_grad`.

## Fuentes

- [The Origin of the Method of Steepest Descent — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0315086096921461)
- [Iterative methods for linear systems of equations: A brief historical journey — arXiv](https://arxiv.org/pdf/1908.01083)
- [A Gentle Introduction to torch.autograd — PyTorch docs](https://docs.pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html)
- Klein, *Coding the Matrix*, Sección 8.4.6-8.4.7 (PDF local)
