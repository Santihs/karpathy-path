---
tags: [phase-0, coding-the-matrix, phase-1, machine-learning, pytorch, perceptron]
date_resolved: 2026-08-07
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Classifier lineal (dot product + signo) — ¿es lo mismo que hace PyTorch?

**Duda:** en el lab de Cap 8 (WDBC breast cancer), el classifier es `C(y) = signo(w·y)`. ¿PyTorch usa este mismo mecanismo por debajo?

## Sí, es exactamente el mismo mecanismo — es el perceptrón clásico

- `torch.sign(x)` existe tal cual, elementwise: `1 si x>0, 0 si x=0, -1 si x<0` — mismo comportamiento que `signum(u)` del lab.
- `nn.Linear(D, 1)` calcula `y = w·x + b` — dot product del input contra un weight vector, más bias opcional. Es el mismo `h(y) = w·y` del libro (Klein no usa bias en este lab, PyTorch sí lo ofrece por defecto).
- Dot product contra w + función de signo/step para decidir la clase = **perceptrón clásico**, el ancestro directo de las redes neuronales modernas. `nn.Linear` seguido de `torch.sign` (o `torch.sigmoid` + threshold en versiones más suaves) ES un perceptrón implementado en PyTorch.

## La diferencia real: cómo se busca w, no el mecanismo

- **Klein (este lab):** gradient descent manual, escrito a mano en Python/Vec — se ve cada paso del cálculo del gradiente y del ajuste de w.
- **PyTorch:** mismo gradient descent, pero automatizado — `loss.backward()` calcula el gradiente vía autograd (el motor de diferenciación automática, el mismo patrón que se va a ver en micrograd, Phase 1), y `optimizer.step()` actualiza w. Este lab es el "modo manual" de exactamente lo que PyTorch hace con una línea de código.

## Fuentes

- [torch.sign — PyTorch docs](https://pytorch.org/docs/stable/generated/torch.sign.html)
- [nn.Linear in PyTorch: Shapes, Bias, and Examples — Kanaries docs](https://docs.kanaries.net/topics/Python/nn-linear)
- [Linear Classifiers and the Perceptron — CMU 10-601 slides](https://www.cs.cmu.edu/~tom/10601_sp08/slides/perceptron-2-4-2008.pdf)
- Klein, *Coding the Matrix*, Sección 8.4.3 (PDF local)
