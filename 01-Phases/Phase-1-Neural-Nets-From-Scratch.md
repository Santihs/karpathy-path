---
tags: [phase-1, neural-nets, backprop, autograd]
status: not_started
---

# Phase 1 — Neural Networks from Scratch

> **Goal:** Backprop and training loops understood at the tensor level — not as framework magic.
> The single most important phase. Everything after depends on what you build here.

## What to nail

- [[Micrograd-Autograd-Engine]] — build a tiny autograd engine; backprop stops being magic here
- [[Backpropagation-Derivation]] — derive it on paper for a 2-layer MLP
- [[Non-Linearities-Why-Needed]] — why ReLU/tanh, what happens without them
- [[Vanishing-Gradients]] — what they are, why they kill deep nets, how they're mitigated
- [[Optimizers-Adam-vs-SGD]] — what Adam actually does differently from plain SGD

## Resources (in order)

1. [Neural Networks: Zero to Hero — Karpathy YouTube playlist](https://karpathy.ai/zero-to-hero.html)
   - micrograd → makemore bigram → makemore MLP → makemore RNN/GRU → makemore Transformer
2. [karpathy/micrograd (GitHub)](https://github.com/karpathy/micrograd)
3. [karpathy/makemore (GitHub)](https://github.com/karpathy/makemore)
4. [CS231n notes — backprop and optimization](http://cs231n.stanford.edu/)

## What to build

- Reimplement micrograd **without looking at source**, then diff and understand every deviation
- Build makemore bigram model on a custom dataset (not just names — try your own text or code)
- Build the MLP version of makemore on the same custom dataset

## Validation checkpoint

- Derive backprop for a 2-layer MLP on paper, no notes
- Explain why we need non-linearities, what vanishing gradients are, and why Adam beats SGD
- Use Claude as a Socratic oral examiner: *"Quiz me on backprop like a PhD oral exam, push back when I'm vague, don't let me move on until I get it right"*

## Links to topic notes

- [[Micrograd-Autograd-Engine]]
- [[Backpropagation-Derivation]]
- [[Non-Linearities-Why-Needed]]
- [[Vanishing-Gradients]]
- [[Optimizers-Adam-vs-SGD]]
