---
tags: [phase-4, finetuning, rlhf, dpo, reasoning, alignment]
status: not_started
---

# Phase 4 — Finetuning, Instruction-Tuning, RLHF/DPO, Reasoning

> **Goal:** Understand how a base model becomes "ChatGPT-like" — and how reasoning models (DeepSeek-R1-style) are built.

## What to nail

- [[Instruction-Finetuning-SFT]] — supervised finetuning, Alpaca-style prompt templates
- [[RLHF-PPO-Mechanics]] — reward model, PPO loop, why it's expensive
- [[DPO-vs-RLHF]] — what DPO optimizes differently, why it became popular (no separate reward model)
- [[LoRA-QLoRA]] — parameter-efficient finetuning mechanics
- [[Chain-of-Thought-Inference-Scaling]] — what CoT actually changes about generation mechanistically
- [[Reasoning-From-Scratch]] — inference-time scaling, RL for reasoning, distillation

## Resources (in order)

1. Raschka slides — visual breakdown: pretraining → instruction finetuning → preference tuning
2. [rasbt/LLMs-from-scratch — Chapter 7 + GPT-4-based eval notebook](https://github.com/rasbt/LLMs-from-scratch)
3. [rasbt/reasoning-from-scratch (GitHub)](https://github.com/rasbt/reasoning-from-scratch) — mirroring DeepSeek-R1/thinking model construction
4. [HuggingFace TRL docs](https://huggingface.co/docs/trl/index) — PPO and DPO hands-on
5. [HuggingFace RLHF explainer blog](https://huggingface.co/blog/rlhf)
6. [Sebastian Raschka Substack](https://magazine.sebastianraschka.com/) — best free current writing on finetuning/RLHF alternatives
7. [Fine-tuning & RL for LLMs: Intro to Post-training (DeepLearning.AI, Sharon Zhou)](https://www.deeplearning.ai/courses/fine-tuning-and-reinforcement-learning-for-llms-intro-to-post-training)

## What to build

- Take a small open base model (Qwen or small Llama variant) and instruction-finetune with LoRA on a custom dataset
- Implement a tiny DPO loop on a toy preference dataset (~few hundred examples) — feel the mechanics
- Run reasoning-from-scratch's inference-time scaling techniques on a small model, measure accuracy delta

## Validation checkpoint

- Explain SFT vs. RLHF (PPO) vs. DPO: what each optimizes, why DPO became popular
- Explain mechanistically what chain-of-thought and inference-time scaling actually change about generation

## Links to topic notes

- [[Instruction-Finetuning-SFT]]
- [[RLHF-PPO-Mechanics]]
- [[DPO-vs-RLHF]]
- [[LoRA-QLoRA]]
- [[Chain-of-Thought-Inference-Scaling]]
