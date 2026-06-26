---
tags: [phase-3, pretraining, scaling, data-pipeline]
status: not_started
---

# Phase 3 — Pretraining at Small Scale

> **Goal:** Actually pretrain something — even tiny. This is what almost nobody does, which is exactly why it's valuable.

## What to nail

- [[Data-Pipeline-FineWeb-Edu]] — dedup, filtering, quality vs. quantity tradeoffs
- [[Scaling-Laws-Intuition]] — Chinchilla intuition, how compute/data/params relate
- [[Compute-Cost-Tradeoffs]] — why frontier training costs millions while your run costs $100
- [[Tokenizer-Training]] — training your own tokenizer vs. borrowing one

## Resources

1. [karpathy/nanochat (GitHub)](https://github.com/karpathy/nanochat) — "The best ChatGPT $100 can buy"
   - Full pipeline: tokenizer → pretraining → midtraining → SFT → eval → inference → web UI
   - ~$15–48 on spot H100 instances; speedrun leaderboard active
2. [karpathy/nanoGPT (GitHub)](https://github.com/karpathy/nanoGPT) — simpler pretraining-only version if nanochat feels too large at first
3. [LitGPT (Lightning AI)](https://github.com/Lightning-AI/litgpt) — clean hackable code for various open architectures
4. Raschka slides PDF — actual token counts and data mixtures for GPT-3, LLaMA 1/2/3, Phi-3

## What to build

- Run `nanochat/speedrun.sh` end to end on a rented GPU box (Lambda, RunPod, etc.)
- Talk to your own trained model
- Change `--depth` and observe how hyperparameters scale — best lived intuition for scaling laws

## Validation checkpoint

- Explain with actual numbers why frontier training costs millions while your run cost $100
- Describe the FineWeb-Edu data pipeline: why dedup matters, quality vs. quantity tradeoffs
- Because you used it — not because you read about it

## Links to topic notes

- [[Scaling-Laws-Intuition]]
- [[Compute-Cost-Tradeoffs]]
- [[Data-Pipeline-FineWeb-Edu]]
