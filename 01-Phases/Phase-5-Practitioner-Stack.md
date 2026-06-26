---
tags: [phase-5, huggingface, vllm, evaluation, practitioner]
status: not_started
---

# Phase 5 — Modern Practitioner Stack

> **Goal:** Fluency with the tools real teams use. "I built one from scratch" → "I can also ship with the standard tools."

## What to nail

- [[HuggingFace-Transformers-API]] — tokenizers, models, pipelines, datasets
- [[vLLM-Inference-Serving]] — fast LLM serving, paged attention, why it's the standard
- [[PEFT-LoRA-In-Practice]] — HF PEFT library, QLoRA 4-bit, adapter merging
- [[Quantization-Bitsandbytes]] — 8-bit/4-bit loading, when to use vs. full precision
- [[Weights-and-Biases-Tracking]] — experiment tracking discipline
- [[LM-Evaluation-Harness]] — run real benchmarks (MMLU, ARC, GSM8K) against your own models

## Resources

1. [HuggingFace LLM Course (free)](https://huggingface.co/learn/llm-course) — transformers, tokenizers, datasets, finetuning, alignment
2. [HuggingFace Agents Course](https://huggingface.co/learn/agents-course)
3. [PyTorch for Deep Learning Professional Certificate (DeepLearning.AI)](https://www.deeplearning.ai/courses/pytorch-for-deep-learning-professional-certificate)
   - Course 3 covers Transformers built from multi-head attention + ONNX/MLflow/pruning/quantization
4. [Transformers in Practice (DeepLearning.AI, Sharon Zhou)](https://www.deeplearning.ai/courses/transformers-in-practice) — KV caching, flash attention, quantization for production
5. [vLLM docs](https://docs.vllm.ai/)
6. [PEFT docs](https://huggingface.co/docs/peft/index)
7. [bitsandbytes docs](https://huggingface.co/docs/bitsandbytes/index)
8. [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)

## What to build

- Take your Phase 4 finetuned model → run lm-evaluation-harness → get real numbers, not vibes
- Reproduce one benchmark result from a paper you've read, even approximately
- Deploy a model on vLLM locally and profile throughput

## Validation checkpoint

- Real benchmark numbers from lm-evaluation-harness on your own model
- Reproduce a paper benchmark result

## Links to topic notes

- [[HuggingFace-Transformers-API]]
- [[vLLM-Inference-Serving]]
- [[PEFT-LoRA-In-Practice]]
- [[Quantization-Bitsandbytes]]
- [[LM-Evaluation-Harness]]
