---
tags: [phase-0, linear-algebra, cramers-rule, determinant, shear]
date_resolved: 2026-07-28
---

# Cramer's rule: shear (no rotación), quién la creó, y por qué importa si Gauss es más rápido

## Pregunta
Confusión sobre la "matriz que gira en X grados" en la derivación geométrica de Cramer's rule (3B1B ch12), quién llegó a la conclusión, por qué importa si Gaussian elimination es más rápido.

## Respuesta

**No es una rotación — es un shear (corte).** El video nunca rota nada; usa el principio de Cavalieri: un shear desliza un paralelogramo en la dirección de uno de sus lados sin cambiar su área (base × altura se mantiene igual).

**Derivación concreta.** Sistema A·x = b, A = [[a,b],[c,d]], x=[x,y] desconocido.

Como b = x·col1 + y·col2, el paralelogramo (col1, b) se puede "deslizar" (shear, sin rotar) hasta (col1, y·col2) sin cambiar su área — la componente x·col1 está en la misma dirección que col1 y no aporta área extra.

- área(col1, b) = área(col1, y·col2) = y · área(col1, col2) = y · det(A)
- **y = área(col1, b) / det(A)** — análogo para x con área(b, col2)/det(A)

Esa es la fórmula de Cramer, derivada sin álgebra — solo geometría de áreas.

**Quién la creó:** Gabriel Cramer, matemático suizo, publicada en 1750. El video de 3B1B no cubre historia, solo la intuición geométrica de por qué la fórmula es cierta.

**Por qué importa si Gauss es más rápido:** el propio video lo dice explícito — *"Cramer's rule is not the best way to compute solutions to linear systems of equations. Gaussian elimination, for example, will generally be faster, especially for larger matrices."* Confirmado: no es la herramienta práctica (`torch.linalg.solve` usa LU decomposition vía Gauss, no Cramer). El valor acá es conceptual — refuerza la relación área↔determinante ya vista en [[Linear-Algebra-Basics]] ch9-11 (dualidad), y prepara terreno para eigenvalues/eigenvectors (ch14), donde el determinante vuelve a ser pieza central.

## Fuentes
- [Cramer's rule, explained geometrically | 3Blue1Brown](https://www.3blue1brown.com/lessons/cramers-rule/)
- [Cramer's rule - Wikipedia](https://en.wikipedia.org/wiki/Cramer's_rule)
