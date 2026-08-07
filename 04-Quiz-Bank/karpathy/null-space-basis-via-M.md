---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - gaussian-elimination
  - null-space
self-explain: true
noteId: 1786145495351
---
Dada A y M tal que MA=U está en echelon form, ¿cómo se extrae una base del null space de A^T ({v : v·A=0})?

---

Para cada fila u_i de U que es el vector cero, la fila correspondiente b_i de M cumple b_i·A=0 — esas filas de M son la base. Son independientes por ser filas de M (invertible), y generan todo el espacio por el Rank-Nullity Theorem (m = rank(A) + nullity(A^T) = filas no-cero + filas cero de U).

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.5 — Base del null space`
