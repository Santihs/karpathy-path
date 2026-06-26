---
tags: [phase-2, transformers, attention]
status: seed
first_learned: null
last_reviewed: null
confidence: 0/5
---

# Self-Attention — Q, K, V

> Seed note — fill in after coding attention from scratch in Phase 2.

## Core concepts to capture

- **Q (Query)**: "what am I looking for?"
- **K (Key)**: "what do I contain / advertise?"
- **V (Value)**: "what do I actually pass on if selected?"
- Attention score: `softmax(QKᵀ / √d_k) * V`
- Why scale by √d_k: without it, dot products grow large in high dimensions → softmax saturates → gradients vanish
- Causal masking: future tokens masked to -inf so the model can't cheat during training

## Why it matters for AI

Self-attention is the core mechanism that replaced RNNs. It allows every token to attend to every other token in one parallelizable operation. Understanding it mechanistically (not just using it) is the threshold between user and practitioner.

## Resources

- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762)
- [karpathy/nanoGPT — model.py](https://github.com/karpathy/nanoGPT)

## Doubts Resolved

<!-- Link any resolved doubts from /06-Doubts-Resolved/ here -->
