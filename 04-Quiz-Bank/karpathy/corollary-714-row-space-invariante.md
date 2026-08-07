---
tags:
  - repo-karpathy
  - phase-0
  - coding-the-matrix
  - gaussian-elimination
  - duality
self-explain: true
noteId: 1786145495277
---
Explica el Corollary 7.1.4: por qué Row(MA) = Row(A) cuando M es invertible.

---

Dos inclusiones: Row(MA)⊆Row(A) por el Lemma 7.1.3 directo (con N=M). Row(A)⊆Row(MA) aplicando el mismo lemma con N=M⁻¹ sobre B=MA: M⁻¹B = M⁻¹(MA) = (M⁻¹M)A = IA = A, entonces Row(A)⊆Row(B)=Row(MA). Ambas inclusiones juntas → igualdad.

Ref: `02-Topics/Coding-the-Matrix-Gaussian-Elimination.md — 7.1.5-7.1.6 — Por qué el algoritmo es correcto`
