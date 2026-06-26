---
tags: [phase-0, math, calculus, gradients]
status: seed
first_learned: null
last_reviewed: null
confidence: 0/5
---

# Calculus — Derivatives and Gradients

> Seed note — fill in after Phase 0 math work and Phase 1 micrograd.

## Core concepts to capture

- Derivative: rate of change of a function at a point
- Gradient: vector of partial derivatives — points in the direction of steepest ascent
- Chain rule: how derivatives compose through nested functions — **this is backpropagation**
- Why we follow the *negative* gradient: we want to minimize loss, not maximize it

## The key insight

The gradient descent update rule `θ = θ - lr * ∇L` is the entire mechanism behind training. Everything in Phase 1 is about understanding this line at every layer simultaneously.

## Why it matters for AI

Backpropagation is automatic differentiation applied via the chain rule through a computation graph. Once you build micrograd, this stops being abstract.

## Resources

- [3Blue1Brown — Essence of Calculus](https://www.3blue1brown.com/topics/calculus)
- [karpathy/micrograd](https://github.com/karpathy/micrograd) — chain rule made concrete

## Doubts Resolved

<!-- Link any resolved doubts from /06-Doubts-Resolved/ here -->
