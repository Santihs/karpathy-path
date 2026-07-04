---
tags: [phase-0, coding-the-matrix, linear-algebra, pytorch, linalg]
date_resolved: 2026-07-03
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Sustitución hacia atrás — para qué sirve y si PyTorch la usa

**Duda:** ¿para qué sirve backward substitution, cómo se llama en español, en qué caso se usa, y lo usa PyTorch por debajo?

## Para qué sirve

Resolver `Ax=b` sin calcular la inversa de `A` — invertir es $O(n^3)$ y numéricamente inestable. Si `A` ya es triangular, resolver es directo y $O(n^2)$.

## Nombre en español

"Sustitución hacia atrás" o "sustitución regresiva" — Klein la llama *backward substitution* (Sec. 2.11.2 del libro), mismo concepto.

## Cuándo se usa

1. Sistema ya triangular (el caso implementado en `triangular.py`) — se aplica directo.
2. Sistema general `Ax=b` — se factoriza `A=LU` (LU decomposition, dos matrices triangulares). Después: forward substitution con `L` (triangular inferior) resuelve un sistema intermedio, backward substitution con `U` (triangular superior) da la solución final. Es el método estándar en producción.

## ¿PyTorch la usa por debajo? Sí, confirmado

`torch.linalg.solve` llama a LAPACK:
- `getrf` — factorización LU con pivoteo parcial (`A = P·L·U`)
- `getrs` — resuelve usando esa factorización, que internamente hace forward substitution (con `L`) + backward substitution (con `U`)

Nuestro `triangular_solve_n`/`triangular_solve` (en `05-Projects/coding-the-matrix/src/coding_the_matrix/triangular.py`) es la mitad final ("backward") de ese pipeline, en su forma más simple: sin pivoteo, un solo triangular.

## Fuentes

- [torch.linalg.solve — PyTorch docs](https://docs.pytorch.org/docs/stable/generated/torch.linalg.solve.html)
- [How does torch.linalg.solve work under the hood? — PyTorch Forums](https://discuss.pytorch.org/t/how-does-torch-linalg-solve-work-under-the-hood/203330)
- [torch.linalg.lu_factor — PyTorch docs](https://docs.pytorch.org/docs/stable/generated/torch.linalg.lu_factor.html)
- Klein, *Coding the Matrix*, Sec. 2.11 (PDF local, verificado con pdftotext)
