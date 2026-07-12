---
tags: [phase-0, linear-algebra, matrix-multiplication, determinant, inverse, null-space, rank]
date_added: 2026-06-27
last_tested: 2026-07-12
---

Q: What does multiplying two matrices $A \cdot B$ represent geometrically?
A: Composing two transformations — apply B first, then A. The result is a single matrix encoding both in sequence.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: Why does $AB \neq BA$ in general?
A: Because the order of transformations matters geometrically. "Rotate then shear" deforms space differently than "shear then rotate" — the second transformation acts on an already-transformed space.

<!-- srs: ease=2.5 interval=1 due=2026-07-13 lapses=0 last_seen=2026-07-12 -->

---

Q: What is the determinant of a matrix, geometrically?
A: The scale factor by which the transformation stretches or shrinks area (2D) or volume (3D). Every region in space gets multiplied by this factor.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: What does det(A) = 0 mean geometrically? And for solving equations?
A: Space was compressed to a lower dimension (line, plane, or point). The transformation is not invertible — information is permanently lost. For $A\vec{x} = \vec{v}$, no unique solution exists.

<!-- srs: ease=2.5 interval=1 due=2026-07-08 lapses=0 last_seen=2026-07-07 -->

---

Q: What is the null space (kernel) of a matrix?
A: The set of all input vectors that get mapped to the zero vector (origin) after the transformation. When det ≠ 0, only $\vec{0}$ itself is in the null space. When det = 0, a whole line/plane of vectors get destroyed.

<!-- srs: ease=2.5 interval=1 due=2026-07-08 lapses=0 last_seen=2026-07-07 -->

---

Q: What is the rank of a matrix?
A: The number of dimensions in the output (column space). Rank 3 = full 3D output. Rank 2 = output is a plane. Rank 1 = output is a line.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: What is the formula for the inverse of a 2×2 matrix $\begin{bmatrix}a&b\\c&d\end{bmatrix}$?
A: $A^{-1} = \frac{1}{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$. Steps: swap diagonal, negate off-diagonal, divide by det.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: What does a 3×2 matrix do geometrically?
A: Takes a 2D input and maps it into 3D space — it embeds a plane inside a higher-dimensional space. Columns = input dims, rows = output dims.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: What is the dimension rule for multiplying matrices?
A: $(m \times n) \cdot (n \times p) = (m \times p)$. The inner dimensions must match; the outer dimensions give the result shape.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: If $A$ is a neural network weight matrix with shape (256 × 784), what is it doing geometrically?
A: Transforming a 784-dimensional input vector into a 256-dimensional output — a nonsquare linear transformation that projects from a higher to a lower dimensional space.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->

---

Q: What does $\det(AB) = \det(A) \times \det(B)$ mean intuitively?
A: If you compose two transformations, the total area/volume scaling equals the product of each individual scaling. Scale by 3 then by 2 = scale by 6 total.

<!-- srs: ease=2.5 interval=1 due=2026-07-06 lapses=0 last_seen=none -->
