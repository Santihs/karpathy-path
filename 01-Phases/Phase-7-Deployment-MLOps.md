---
tags: [phase-7, deployment, mlops, serving]
status: not_started
---

# Phase 7 — Deployment & MLOps for AI Systems

> **Goal:** Ship and serve models/agents reliably. The model is only half the system.

## What to nail

- [[vLLM-Serving-Setup]] — production LLM serving, paged attention, batching
- [[Ollama-Local-Serving]] — local self-hosted inference for dev/testing
- [[HuggingFace-Spaces-Gradio]] — fastest path to a public demo
- [[Latency-Cost-Batching-Tradeoffs]] — the engineering tradeoffs that matter in prod
- [[Model-Monitoring-Basics]] — what to watch, what pages someone at 3am

## Resources

1. [vLLM docs](https://docs.vllm.ai/)
2. [Ollama](https://ollama.com/)
3. [HuggingFace Inference Endpoints / Spaces docs](https://huggingface.co/docs/inference-endpoints/index)
4. [LitGPT serving guide (Lightning AI)](https://lightning.ai/lightning-ai/studios/litgpt-serve)
5. Standard SRE/MLOps concepts: monitoring, latency/cost tradeoffs, batching, caching, fallback model routing

## What to build

- Take one finetuned/pretrained model → deploy behind an API + simple Gradio UI on HF Spaces, end to end
- Mirror the codewithdark-git repo's Week 4 deployment step

## Validation checkpoint

- Public demo link (HF Spaces) for one of your trained models — actually deployed, not just "it works locally"

## Links to topic notes

- [[vLLM-Serving-Setup]]
- [[Ollama-Local-Serving]]
- [[Latency-Cost-Batching-Tradeoffs]]
