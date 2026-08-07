---
tags:
  - repo-karpathy
  - phase-0
  - linear-algebra
  - dot-product
  - duality
  - cross-product
noteId: 1786138502052
---
En la derivación de v×w por dualidad (Ch11), una vez que sabés que existe p tal que f(x)=p·x, ¿cómo encontrás las componentes de p?

---

Expandís det([x,v,w]) por cofactores en la columna x, te queda una expresión p₁x+p₂y+p₃z. Comparás término a término con p·x = p₁x+p₂y+p₃z — cada coeficiente del determinante expandido ES la componente correspondiente de p.

Ref: `02-Topics/Linear-Algebra-Basics.md — Ch 11 — Cross Product como Dualidad`
