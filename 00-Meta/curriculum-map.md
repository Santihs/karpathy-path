# Curriculum Map

> Source of truth: [[AI_Roadmap_From_Developer_to_Karpathy_Level]]
> Progress data: [[progress.json]]

## The Stack

```
Theory → From-scratch implementation → Real tools → Deploy → Specialize
```

## Phases at a Glance

| Phase | Focus | Key Build | Weeks |
|-------|-------|-----------|-------|
| [[Phase-0-Math-Refresh]] | Linear algebra, calculus, probability, PyTorch tensors | PyTorch 60-min blitz | 1–3 |
| [[Phase-1-Neural-Nets-From-Scratch]] | Backprop, autograd, training loops | micrograd + makemore reimplementation | 2–3 |
| [[Phase-2-GPT-From-Scratch]] | Transformers, attention, tokenization | Tiny GPT trained on own dataset | 2–3 |
| [[Phase-3-Pretraining]] | Data pipelines, compute, scaling laws | nanochat speedrun (~$100 GPU run) | 2–3 |
| [[Phase-4-Finetuning-RLHF-DPO]] | SFT, RLHF, DPO, reasoning | LoRA finetune + tiny DPO loop | 2–3 |
| [[Phase-5-Practitioner-Stack]] | HF ecosystem, vLLM, eval harnesses | Run lm-evaluation-harness on own model | 2–3 |
| [[Phase-6-Agents]] | Agent loops, tool use, orchestration | Minimal coding agent from scratch | 2–3 |
| [[Phase-7-Deployment-MLOps]] | Serving, monitoring, cost/latency | Deploy finetuned model to HF Spaces | 1–2 |
| [[Phase-8-Specialization]] | Pick a lane and go deep | TBD after Phase 7 | indefinite |

## Key People / Resources

| Person | Role in Roadmap |
|--------|----------------|
| Andrej Karpathy | North star; micrograd, makemore, nanoGPT, nanochat |
| Sebastian Raschka | Books: LLMs from Scratch + Reasoning from Scratch; best free blog |
| Jay Alammar | Visual explainers: Illustrated Transformer, etc. |
| Andrew Ng / DeepLearning.AI | Conceptual foundation (Phase 0) + PyTorch cert (Phase 5) |

## Specialization Tracks (Phase 8 options)

- **Applied AI Engineering / Agents** — fastest path to employment given dev background
- **Research / Pretraining** — highest ceiling; where Karpathy actually went
- Applied ML / Finetuning
- Infra / Systems (CUDA, distributed training)
- Alignment / Safety
