# Reference Library — Curated Math & DL Books

Analysis of the shared Drive folder ("DL", 16 PDFs) against the karpathy-path roadmap.
Decision: **PDFs are NOT committed to this repo** (copyright risk on GitHub + binary bloat in git history).
Instead, this note tracks which books complement the path, when to use them, and where the **legal free versions** live.

Analyzed: 2026-07-02

---

## Tier 1 — Directly complements the path (use these)

| Book | Phase | Why | Legal free version |
|---|---|---|---|
| **Linear Algebra Done Right** — Axler, 4th ed | Phase 0 | Proof-based counterpart to 3B1B's intuition. Use as *lookup*, not cover-to-cover: read a chapter when a 3B1B concept feels hand-wavy (e.g. eigenvalues, duality). | Open access: https://linear.axler.net/ |
| **Introduction to Probability** — Blitzstein & Hwang, 2nd ed | Phase 0 | Best-in-class for the probability block (distributions, expectation → cross-entropy). Pairs with the Stat 110 lectures. | Free from authors: http://probabilitybook.net |
| **Deep Learning** — Goodfellow, Bengio, Courville | Phases 1–3 | *The* theory reference behind Karpathy's videos. Ch 6–8 (MLPs, regularization, optimization) map directly onto micrograd/makemore. | Free HTML: https://www.deeplearningbook.org |
| **Math and Architectures of Deep Learning** — Chaudhury | Phases 0–1 | Bridges math ↔ PyTorch code, exactly the Phase 0 → Phase 1 transition. Nice-to-have, not essential. | Paid (Manning) — no legal free copy |

## Tier 2 — Reference / Phase 8 material (park for later)

| Book | When | Why | Legal free version |
|---|---|---|---|
| **Convex Optimization** — Boyd & Vandenberghe | Phase 1 (optimizers) → Phase 8 | Answers *why gradient descent works*. Overkill for the main path; the right depth for the `research_pretraining` or `alignment_safety` tracks. | Free from author: https://web.stanford.edu/~boyd/cvxbook/ |
| **Understanding Machine Learning** — Shalev-Shwartz & Ben-David | Phase 8 | Learning theory (PAC, VC dimension) — "prove algorithm limits" territory. Zero use before specialization. | Free from author: https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/ |

## Tier 3 — Redundant with the path (skip)

- **Deep Learning from Scratch** — Weidman. Covers exactly what Phase 1 (micrograd, makemore) does, but Karpathy's build-it-live format is strictly better for this path. Skip.

## Tier 4 — Not relevant to this path (graduate pure math)

Kreyszig *Functional Analysis* · Hall *Lie Groups, Lie Algebras & Representations* · Fulton & Harris *Representation Theory* · Artin *Algebra* · Tu *Introduction to Manifolds* · Tao *Analysis I* · Doran & Lasenby *Geometric Algebra for Physicists* · Dorst et al. *Geometric Algebra for Computer Science* · Hairer et al. *Geometric Numerical Integration*

These are real classics, but for math-PhD-track depth (representation theory, differential geometry, functional analysis) that no phase of this roadmap touches. Keeping them "just in case" is collecting, not learning. If Phase 8 lands on `research_pretraining` or `alignment_safety`, revisit Tao *Analysis I* first — the rest stay out.

---

## Usage rule

Books here are **lookup material, not the path**. The roadmap's spine stays: Karpathy videos + notebooks + Raschka. Open a Tier 1 book only when a concept in the main path needs more depth, then log what was learned to `/02-Topics/` as usual.
