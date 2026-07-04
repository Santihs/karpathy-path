---
tags: [phase-0, coding-the-matrix, linear-algebra, dot-product, triangular-solve]
date_resolved: 2026-07-03
source_pdf: "00-Meta/resources/Philip N. Klein-Coding the Matrix_ Linear Algebra through Computer Science Applications-Newtonian Press (2013).pdf"
---

# Pivote cero en backward substitution — visual + dónde entra el dot-product

**Duda:** ¿qué pasa si un pivote (`rowlist[i][i]`) es cero? ¿Dónde entra el dot-product en el algoritmo?

## Sí, el dot-product es el corazón del algoritmo

La línea clave es `rowlist[i] * x` dentro del loop — `Vec.__mul__` entre dos `Vec` ES el dot-product (`Coding-the-Matrix-Vectors.md`, sección 10). El truco: `x` empieza en cero y se va llenando de atrás para adelante, así que el dot-product automáticamente "ignora" las variables que todavía no conocés (valen 0, no aportan a la suma) y solo pesa las que ya resolviste.

## Visual — matriz 4×4 del Example 2.11.1

```
fila 0: [ 1   0.5  -2    4  ] · x = -8
fila 1: [ 0    3    3    2  ] · x =  3
fila 2: [ 0    0    1    5  ] · x = -4
fila 3: [ 0    0    0    2  ] · x =  6
```

Orden de resolución: empezás por la fila 3 (arriba hacia abajo en el diagrama, pero última en el loop `reversed(range(n))`).

**Iteración i=3** — `x = [0,0,0,0]` (todo desconocido todavía)
```
rowlist[3]·x = 0*x0 + 0*x1 + 0*x2 + 2*x3  →  con x3 aún 0 → dot = 0
x[3] = (6 - 0) / 2 = 3
```
Ahora `x = [0,0,0,3]`.

**Iteración i=2** — dot-product usa la parte YA conocida de x, ignora el resto (siguen en 0):
```
rowlist[2]·x = 0*x0 + 0*x1 + 1*x2 + 5*x3
             = 1*0 + 5*3        (x2 todavía 0, se resta después)
             = 15
x[2] = (-4 - 15) / 1 = -19
```
Ahora `x = [0,0,-19,3]`.

**Iteración i=1**:
```
rowlist[1]·x = 3*x1 + 3*x2 + 2*x3 = 3*0 + 3*(-19) + 2*3 = -57+6 = -51
x[1] = (3 - (-51)) / 3 = 18
```

**Iteración i=0**:
```
rowlist[0]·x = 1*x0 + 0.5*x1 - 2*x2 + 4*x3 = 0 + 9 + 38 + 12 = 59
x[0] = (-8 - 59) / 1 = -67
```

Resultado: `x = [-67, 18, -19, 3]` — coincide con el test (`test_triangular_solve_n_book_example`).

**Por qué funciona el truco del dot-product:** en cada iteración, `x` tiene ceros exactamente en las posiciones todavía no resueltas — y esas posiciones son justo las que la fila actual tiene coeficiente conocido pero valor desconocido. El dot-product suma "coeficiente × valor", así que las posiciones no resueltas aportan `coef × 0 = 0` automáticamente. No hace falta lógica especial para "ignorar lo desconocido" — es gratis, viene de la definición de dot-product.

## Caso pivote cero (Prop. 2.11.6)

Si `rowlist[i][i] == 0` en algún punto, la división `/rowlist[i][i]` es imposible — y el libro prueba que esto NO es solo un problema del algoritmo: matemáticamente, para algún `b` posible, el sistema no tiene ninguna solución (ver imagen previa, prueba por inducción con `b` concentrado en la posición del pivote cero).

**Qué hace el código ahora** (`triangular.py`, actualizado):
```python
assert rowlist[i][i] != 0, f"zero pivot at row {i} — no unique solution (Prop. 2.11.6)"
x[i] = (b[i] - rowlist[i] * x) / rowlist[i][i]
```
Falla explícito con mensaje claro, en vez de dejar que un `ZeroDivisionError` genérico salga sin contexto.

**Qué se hace en la práctica cuando la matriz NO es triangular** (caso general): se usa *partial pivoting* — reordenar filas para mover un valor no-cero a la diagonal antes de triangular. Es literalmente la `P` en la factorización `A = P·L·U` que usa LAPACK `getrf` (la rutina detrás de `torch.linalg.solve`, ver [[backward-substitution-pytorch]]). Si ningún reordenamiento arregla el pivote cero, la matriz es genuinamente singular — ahí ya no aplica triangular solve, hace falta mínimos cuadrados (`torch.linalg.lstsq`).

## Ver también

- [[backward-substitution-pytorch]] — para qué sirve, y cómo lo usa `torch.linalg.solve` (LAPACK getrf/getrs)
- `05-Projects/coding-the-matrix/tests/test_triangular.py::test_triangular_solve_n_zero_pivot_raises` — test que verifica el assert
