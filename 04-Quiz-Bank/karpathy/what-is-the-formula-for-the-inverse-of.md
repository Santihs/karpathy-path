---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - matrix-multiplication
  - determinant
  - inverse
  - null-space
  - rank
noteId: 1785651975175
---
What is the formula for the inverse of a 2×2 matrix $\begin{bmatrix}a&b\\c&d\end{bmatrix}$?

---

$A^{-1} = \frac{1}{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$. Steps: swap diagonal, negate off-diagonal, divide by det.

Ref: `02-Topics/Linear-Algebra-Basics.md — Ch 7 — Inverse Matrices, Column Space, Null Space`
