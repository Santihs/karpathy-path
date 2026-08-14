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
What is the formula for the inverse of a 2x2 matrix [[a,b],[c,d]]?

---

A^-1 = (1/(ad-bc)) * [[d,-b],[-c,a]]. Steps: swap the diagonal (a<->d), negate the off-diagonal entries, divide by det(A)=ad-bc.

Ref: `02-Topics/Linear-Algebra-Basics.md — Ch 7 — Inverse Matrices, Column Space, Null Space`
