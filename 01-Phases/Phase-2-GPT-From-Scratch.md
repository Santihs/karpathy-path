---
tags: [phase-2, transformers, attention, gpt, tokenization]
status: not_started
---

# Phase 2 — Build a GPT from Scratch

> **Goal:** Understand transformers and attention because you coded one — not because you read about it.

## What to nail

- [[Tokenization-BPE]] — byte-pair encoding before relying on tiktoken/transformers
- [[Self-Attention-QKV]] — Q, K, V, why scale by √d_k, what the dot product actually measures
- [[Multi-Head-Attention]] — why multiple heads, what each head can specialize in
- [[Causal-Masking]] — why autoregressive generation needs it
- [[Positional-Encoding]] — why transformers have no inherent sense of order
- [[Transformer-Block-Architecture]] — attention + FFN + residual + layer norm
- [[Layer-Norm-vs-Batch-Norm]] — why LN for sequence models

## Resources (in order)

1. [karpathy/nanoGPT (GitHub)](https://github.com/karpathy/nanoGPT) — read every file
2. [Let's build GPT: from scratch, in code — Karpathy YouTube](https://karpathy.ai/zero-to-hero.html)
3. *Build a Large Language Model (From Scratch)* — Sebastian Raschka, Chapters 2–4
4. [rasbt/LLMs-from-scratch (GitHub)](https://github.com/rasbt/LLMs-from-scratch)
5. [codewithdark-git/Building-LLMs-from-scratch](https://github.com/codewithdark-git/Building-LLMs-from-scratch) — week-by-week study planner
6. [Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762) — read *after* coding attention once
7. [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
8. [karpathy/llm.c (GitHub)](https://github.com/karpathy/llm.c) — GPT-2 in raw C/CUDA; humbling

## What to build

- Implement multi-head self-attention from scratch (no `nn.MultiheadAttention`)
- Implement BPE tokenizer from scratch before touching `tiktoken`
- Train a tiny GPT on: Shakespeare, your own codebase, or your own messages — watch overfit/generalize

## Validation checkpoint

- Explain Q/K/V, why scale by √d_k, what causal masking does, why positional encodings exist
- Run Raschka's free 170-page self-test PDF (chapter-by-chapter, ~30 questions each)
- Ask Claude to review your from-scratch attention implementation and find an intentionally introduced bug

## Links to topic notes

- [[Self-Attention-QKV]]
- [[Multi-Head-Attention]]
- [[Causal-Masking]]
- [[Positional-Encoding]]
- [[Tokenization-BPE]]
- [[Transformer-Block-Architecture]]
