---
tags: [phase-0, math, foundations]
status: in_progress
---

# Phase 0 — Math & ML Refresher

> **Goal:** Comfortable enough with the math vocabulary to read papers and debug training. Not a math degree — just enough.

## What to nail

- [[Linear-Algebra-Basics]] — matrix multiplication, dot products, vectors as points in space
- [[Calculus-Gradients]] — derivatives, gradients, chain rule (this *is* backprop)
- [[Probability-Basics]] — distributions, expectation, cross-entropy, softmax
- [[NumPy-Fundamentals]] — scientific Python foundation
- [[PyTorch-Tensors-Autograd]] — tensors, autograd, first training loop

## Resources (in order)

1. [3Blue1Brown — Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)
2. [3Blue1Brown — Neural Networks series](https://www.3blue1brown.com/topics/neural-networks)
3. [Mathematics for Machine Learning (free book)](https://mml-book.github.io/)
4. [PyTorch 60-minute blitz](https://docs.pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
5. [Andrew Ng — ML Specialization (Coursera)](https://www.coursera.org/specializations/machine-learning-introduction) — use for concepts/math only, not as coding reference

## What to build

- Run the PyTorch blitz end to end, type everything manually (no copy-paste)
- Write a manual matrix multiply in NumPy without using `np.dot`, then verify with `np.dot`

## Validation checkpoint

> Explain out loud with no notes: **"What is a gradient, and why does following its negative direction reduce loss?"**
> If you can't, stay in Phase 0.

## Links to topic notes

- [[Linear-Algebra-Basics]]
- [[Calculus-Gradients]]
- [[Probability-Basics]]
- [[PyTorch-Tensors-Autograd]]
