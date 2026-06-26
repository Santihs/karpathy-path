# From Developer to "Karpathy-Level": A Roadmap to Deeply Understand, Train, and Deploy AI

> **Who this is for:** A working developer who already uses AI agents/tools and wants to go from "user of AI" to "person who understands and can build the thing" — with a real path to specialize afterward (research, applied ML, infra, agents, etc).
> **Format:** Think of this as a PhD advisor's syllabus — phases, not days. Each phase has *what to learn*, *what to build*, *how to validate you actually learned it*, and *where to practice*.

---

## 0. A note on your two reference links

You shared:
- `facebook.com/0xSojalSec`
- `linkedin.com/in/0xsojalsec`

I checked these — they belong to a security/threat-intel social media persona, not an AI/ML educator, course, or research reference. There's nothing there relevant to learning AI/LLMs, so I'm leaving them out of this roadmap rather than padding the file with a dead link. Everything below is a real, currently active resource as of mid-2026.

---

## 1. The North Star: what "Karpathy-level" actually means

Andrej Karpathy's path (Stanford PhD → OpenAI founding member → Tesla AI director → Eureka Labs founder → **now leading pretraining research at Anthropic as of May 2026**) is not really replicable as a credential path. What *is* replicable is his **method**, which his own teaching repeatedly demonstrates:

1. **Build it from scratch before you use the library.** He builds raw Python/PyTorch before `transformers`.
2. **Make it minimal and readable, not "production".** nanoGPT, micrograd, nanochat are all intentionally small.
3. **Go full-stack**: tokenizer → architecture → pretraining → finetuning → inference → serving UI. Not just "the model part."
4. **Ground everything in code you ran yourself**, not just papers you read.

This roadmap is structured the same way: **theory → from-scratch implementation → use-the-real-tools → deploy → specialize.**

---

## 2. Roadmap at a glance

| Phase | Focus | Outcome |
|---|---|---|
| 0 | Math & ML refresher | Comfortable with the vocabulary and the math notation in papers |
| 1 | Neural nets from scratch | You understand backprop and training loops at the tensor level |
| 2 | Build a GPT from scratch | You understand transformers/attention because you coded one |
| 3 | Pretraining at small scale | You've trained a real (tiny) LLM and seen the cost/compute tradeoffs |
| 4 | Finetuning, alignment, RLHF/DPO | You understand how a base model becomes "ChatGPT-like" |
| 5 | Modern practitioner stack | You can use HF, vLLM, LoRA/QLoRA, quantization, eval harnesses fluently |
| 6 | Agents & applied workflows | You can build production AI workflows/agents (your existing dev skill + new depth) |
| 7 | Deployment & MLOps for AI | You can ship and serve models/agents reliably |
| 8 | Specialization tracks | Pick a lane: research, infra, applied/agents, safety/alignment |
| 9 | Validation system | How to *prove* (to yourself and employers) that you actually know this |

---

## 3. Phase 0 — Refresh the foundations (1–3 weeks if you're rusty, skip what you already know)

You're a dev, so skip straight to gaps. You need just enough math to read papers and debug training, not a full math degree.

**Concepts to nail:**
- Linear algebra: matrix multiplication, dot products, vectors/embeddings as points in space
- Calculus: derivatives, gradients, chain rule (this *is* backprop)
- Probability: distributions, expectation, cross-entropy, softmax
- Python scientific stack: NumPy, then PyTorch tensors

**Resources:**
- [3Blue1Brown — Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) and [Neural Networks series](https://www.3blue1brown.com/topics/neural-networks) — best visual intuition available, full stop.
- [Mathematics for Machine Learning (free book, Deisenroth/Faisal/Ong)](https://mml-book.github.io/) — the standard free reference.
- [PyTorch official 60-minute blitz](https://docs.pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html) — get tensors/autograd in your hands.
- **[Andrew Ng — Machine Learning Specialization (DeepLearning.AI/Stanford, recently updated)](https://www.coursera.org/specializations/machine-learning-introduction)** — yes, this still earns its place. It's the best *intuition-first* teacher for what supervised/unsupervised learning, gradient descent, and neural nets actually are conceptually, before you touch a deep learning framework. The lab code leans NumPy/scikit-learn/TensorFlow rather than PyTorch — treat it as the **concepts-and-math layer**, not your coding reference, and you'll get full value without friction later.

**Validate:** You should be able to explain, out loud with no notes: "what is a gradient, and why does following its negative direction reduce loss?" If you can't, stay here.

---

## 4. Phase 1 — Neural networks from absolute scratch (the Karpathy "Zero to Hero" track)

This is the single most important phase. Karpathy's own foundational series — still the best "from zero" material that exists.

**Resources (in order):**
1. [Neural Networks: Zero to Hero (YouTube playlist)](https://karpathy.ai/zero-to-hero.html) — start here, no exceptions.
   - *micrograd*: build a tiny autograd engine — this is where backprop stops being magic.
   - *makemore*: build a character-level language model, several times, with increasing sophistication (bigram → MLP → RNN → GRU → Transformer).
2. [karpathy/micrograd (GitHub)](https://github.com/karpathy/micrograd) — read and reimplement.
3. [karpathy/makemore (GitHub)](https://github.com/karpathy/makemore) — same.
4. [CS231n: Convolutional Neural Networks for Visual Recognition (Stanford, Karpathy's original course)](http://cs231n.stanford.edu/) — even though it's vision-focused, the backprop/optimization fundamentals transfer directly and the notes are exceptional.

**What to build (don't skip this):**
- Reimplement micrograd **without looking at the source**, then compare.
- Build makemore's bigram model, then the MLP version, on your own dataset (not just names — try it on your own text/code).

**Validate:**
- You can derive backprop for a 2-layer MLP on paper.
- You can explain why we need non-linearities, what vanishing gradients are, and why we use Adam over plain SGD.
- Use an LLM (Claude, etc.) as a **Socratic quiz partner**: ask it to "quiz me on backprop and neural net training like a PhD oral exam, ask follow-ups based on my answers, don't let me move on until I get it right." This works far better than just reading.

---

## 5. Phase 2 — Build a GPT from scratch (Transformers, attention, tokenization)

Now the architecture that actually matters today.

**Primary resources:**
1. [karpathy/nanoGPT (GitHub)](https://github.com/karpathy/nanoGPT) — the cleanest, most-copied GPT training repo in existence. Read every file.
2. [Let's build GPT: from scratch, in code, spelled out (YouTube)](https://karpathy.ai/zero-to-hero.html) — Karpathy builds nanoGPT live, line by line.
3. **The book you found** — *Build a Large Language Model (From Scratch)* by Sebastian Raschka:
   - Companion code repo: [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) (the canonical, actively maintained one — 97k+ stars)
   - Free companion slide deck: [sebastianraschka.com/pdf/slides/2024-build-llms.pdf](https://sebastianraschka.com/pdf/slides/2024-build-llms.pdf) (the one you linked — great for the big-picture diagram: Build → Pretrain → Finetune)
   - Manning book page: [manning.com/books/build-a-large-language-model-from-scratch](https://www.manning.com/books/build-a-large-language-model-from-scratch)
   - Free 170-page self-test PDF ("Test Yourself On Build a Large Language Model") — available via the Manning book page, ~30 quiz questions per chapter. **Use this as your exam.**
4. The repo you originally found — [codewithdark-git/Building-LLMs-from-scratch](https://github.com/codewithdark-git/Building-LLMs-from-scratch) — a structured 4-week curriculum built directly on top of Raschka's book, with notebooks already organized week-by-week (tokenization → attention/decoder → training loop → generation/deployment to Hugging Face). Good as a study planner layered on top of the book.
5. ["Attention Is All You Need" (original Transformer paper)](https://arxiv.org/abs/1706.03762) — read it *after* you've coded attention once, not before. It'll click immediately.
6. [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) — best visual companion to the paper.
7. [karpathy/llm.c (GitHub)](https://github.com/karpathy/llm.c) — once comfortable, see GPT-2 training implemented in raw C/CUDA. Humbling and clarifying about what frameworks actually hide from you.

**What to build:**
- Implement multi-head self-attention from scratch (no `nn.MultiheadAttention`).
- Train your own tiny GPT on a small dataset (Shakespeare, your own codebase, your own messages) and watch it overfit/generalize.
- Implement tokenization yourself (byte-pair encoding) before relying on `tiktoken`/`transformers`.

**Validate:**
- Explain Q/K/V, why we scale by √d_k, what causal masking does, and why positional encodings exist.
- Run the 170-page Raschka self-test quizzes per chapter — these are designed exactly for this checkpoint.
- Ask Claude/an LLM to review your from-scratch attention implementation and find the bug if you intentionally introduce one — great calibration exercise.

---

## 6. Phase 3 — Pretraining at small scale (the part almost nobody does, which is why it's valuable)

This is where you stop simulating and actually pretrain something, even if tiny.

**Primary resource — Karpathy's `nanochat` (2025, current, his most important hands-on artifact):**
- [karpathy/nanochat (GitHub)](https://github.com/karpathy/nanochat) — "The best ChatGPT that $100 can buy." A full pipeline: tokenizer → pretraining → midtraining → SFT → eval → inference → web UI, ~8,000 lines, single clean repo.
  - You can train a real, GPT-2-class, talkable model for **~$100 on an 8×H100 box** (or even cheaper on spot instances, ~$15–48).
  - This will eventually be the capstone of Karpathy's **LLM101n** course (in development at Eureka Labs; the original repo is archived but the concept lives on through nanochat).
  - There's an active community speedrun leaderboard for "time to GPT-2-level CORE score" — genuinely fun way to benchmark your understanding against others.
- [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) — simpler, pretraining-only version if nanochat feels like too much at first.

**Context/cost intuition resources:**
- Raschka's slides (same PDF as above) — has the actual token counts and data mixtures used for GPT-3, LLaMA 1/2/3, and Phi-3, with sources. Use this to build real intuition for scale.
- [LitGPT (Lightning AI)](https://github.com/Lightning-AI/litgpt) — for running/pretraining various open architectures with clean, hackable code; referenced directly in Raschka's slides.

**What to build:**
- Run the nanochat `speedrun.sh` end to end on a rented GPU box (Lambda, RunPod, etc.) and actually talk to your own model.
- Try changing `--depth` and observe how every other hyperparameter scales automatically — this is the best lived intuition for "scaling laws" you can get without reading Chinchilla cover to cover.

**Validate:**
- You can explain, with numbers, why pretraining a frontier model costs millions while your run cost $100.
- You can describe the actual data pipeline (FineWeb-Edu shards, why dedup/filtering matters, quality vs. quantity tradeoffs) because you used it, not because you read about it.

---

## 7. Phase 4 — Finetuning, Instruction-tuning, RLHF/DPO/Preference-tuning, and Reasoning

This is "how a base model becomes ChatGPT" — and increasingly, "how a model becomes a *reasoner*."

**Resources:**
1. Raschka's slides — has the clean visual breakdown: pretraining → instruction finetuning → preference tuning, with the Alpaca-style prompt template example.
2. [rasbt/LLMs-from-scratch — Chapter 7 (instruction finetuning) + GPT-4-based eval notebook](https://github.com/rasbt/LLMs-from-scratch) — hands-on code for both finetuning and *evaluating* a finetuned model.
3. **Reasoning models — the newest and most relevant frontier topic (2025 book/repo):**
   - [rasbt/reasoning-from-scratch (GitHub)](https://github.com/rasbt/reasoning-from-scratch) — companion to Raschka's newest book, *Build A Reasoning Model (From Scratch)* (Manning, 2025). Starts from a pretrained base model (Qwen3) and builds up reasoning behavior step by step: inference-time scaling, reinforcement learning, and distillation — mirroring how DeepSeek-R1-style and "thinking" models are actually built.
4. [Hugging Face — Reinforcement Learning from Human Feedback (RLHF) explainer](https://huggingface.co/blog/rlhf) and [TRL library docs](https://huggingface.co/docs/trl/index) for hands-on PPO/DPO.
5. Raschka's blog has deep, free explainers on finetuning and RLHF alternatives — search "magazine.sebastianraschka.com finetuning" and "llm-training-rlhf-and-its-alternatives" for the most current posts (his Substack is consistently the best free, current technical writing on this; check it directly since posts update often: [magazine.sebastianraschka.com](https://magazine.sebastianraschka.com/)).

**What to build:**
- Take a small open base model (e.g. a small Qwen or Llama variant) and instruction-finetune it on a custom dataset using LoRA.
- Implement a tiny DPO loop on a toy preference dataset — even a few hundred examples — to feel the mechanics.
- Try the reasoning-from-scratch repo's inference-time scaling techniques on a small model and measure the accuracy delta.

**Validate:**
- Explain the difference between SFT, RLHF (PPO-based), and DPO — what each optimizes and why DPO became popular (cheaper, no separate reward model needed).
- Explain at a mechanistic level what "chain-of-thought" and "inference-time scaling" actually change about generation, not just that they "make the model think more."

---

## 8. Phase 5 — The modern practitioner stack (what you need to be employable *today*)

This phase is about fluency with the tools real teams use — this is where "I built one from scratch" becomes "I can also ship with the standard tools."

### 8.1 The Andrew Ng / DeepLearning.AI angle, updated for PyTorch (2026)

You specifically asked about this, so here it is properly placed: Ng's original Deep Learning Specialization (Phase 0, above) is conceptually excellent but framework-old (NumPy/TensorFlow-leaning). DeepLearning.AI has since shipped exactly what you're after — current, hands-on, PyTorch-first material. None of these are taught by Ng personally (he's shifted toward agentic/strategy courses), but they're DeepLearning.AI's house style applied to PyTorch, which is the closest equivalent that exists today:

- **[PyTorch for Deep Learning Professional Certificate (DeepLearning.AI, instructor: Laurence Moroney)](https://www.deeplearning.ai/courses/pytorch-for-deep-learning-professional-certificate)** — 3 courses, self-paced, hands-on labs the whole way through:
  - *Course 1 — PyTorch Fundamentals*: tensors, datasets/dataloaders, training loops, your first neural net.
  - *Course 2 — Techniques and Ecosystem Tools*: hyperparameter tuning with Optuna, the PyTorch Profiler, TorchVision for images, Hugging Face for text, transfer learning.
  - *Course 3 — Advanced Architectures and Deployment*: Siamese networks, ResNet/DenseNet, **Transformers built from multi-head attention**, diffusion models, then deployment via ONNX, MLflow, pruning, and quantization.
  - This is functionally "Ng's Deep Learning Specialization, but in PyTorch, current, and carried all the way to deployment." If you only add one DeepLearning.AI resource to this roadmap, make it this one.
- **[How Transformer LLMs Work (DeepLearning.AI, short course)](https://www.deeplearning.ai/courses/how-transformer-llms-work)** — co-taught with the authors of *Hands-On Large Language Models*; complements (don't replace) the from-scratch attention work in Phase 2.
- **[Transformers in Practice (DeepLearning.AI, instructor: Sharon Zhou, VP Eng & AI at AMD)](https://www.deeplearning.ai/courses/transformers-in-practice)** — brand-new in 2026, and a genuinely good fit for where you are: it's explicitly aimed at people who already *use* LLMs/agents and want the internals — autoregressive generation, attention/positional encoding intuition, then KV caching, flash attention, and quantization for production inference. Less "build from scratch," more "understand deeply enough to debug and deploy" — pairs well with Phase 6/7.
- **[Fine-tuning & RL for LLMs: Intro to Post-training (DeepLearning.AI, instructor: Sharon Zhou)](https://www.deeplearning.ai/courses/fine-tuning-and-reinforcement-learning-for-llms-intro-to-post-training)** — maps directly onto Phase 4 above (SFT, RLHF, DPO) but from the applied/production angle rather than the from-scratch-paper angle. Good as a second pass after `rasbt/reasoning-from-scratch` to see how the same ideas get applied at the "shipping an internal copilot" level.

**How to sequence these against the rest of the roadmap:** don't do the PyTorch Professional Certificate *instead of* Phase 1–3's from-scratch work — do it *alongside or right after*. The from-scratch phases build understanding; this certificate builds the muscle memory and ecosystem fluency (Optuna, MLflow, ONNX, profiling) that from-scratch work intentionally skips for the sake of clarity.

**Core libraries/platforms:**
- [Hugging Face — LLM Course (free, huggingface.co/learn/llm-course)](https://huggingface.co/learn/llm-course) — transformers, tokenizers, datasets, fine-tuning, alignment, all current.
- [Hugging Face — Agents Course](https://huggingface.co/learn/agents-course) — current and directly relevant to your agent-building background.
- [PyTorch tutorials](https://docs.pytorch.org/tutorials/) — for anything below the HF abstraction layer.
- [vLLM docs](https://docs.vllm.ai/) — the standard for fast LLM inference serving; learn this for deployment, not just training.
- [PEFT (HF) — LoRA/QLoRA](https://huggingface.co/docs/peft/index) — parameter-efficient finetuning, what you'll actually use in practice instead of full finetunes.
- [bitsandbytes / quantization basics](https://huggingface.co/docs/bitsandbytes/index) — running big models on consumer/limited hardware.
- [Weights & Biases](https://wandb.ai/) — experiment tracking; even small projects benefit from this discipline.

**Evaluation (critical, often skipped):**
- [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) — the standard for running MMLU, ARC, GSM8K, etc. against your own models.
- [AlpacaEval](https://tatsu-lab.github.io/alpaca_eval/) and [LMSYS Chatbot Arena](https://chat.lmsys.org/) — understand how model comparison/leaderboards actually work, since you'll be judged against them eventually.

**Validate:**
- Take a model you finetuned in Phase 4 and run it through lm-evaluation-harness yourself — get real numbers, not vibes.
- Reproduce one benchmark result from a paper you've read, even approximately.

---

## 9. Phase 6 — Agents and applied AI workflows (your natural strength — go deep here)

You already use AI agents. This phase turns "user of agent tools" into "person who understands and designs agent systems."

**Resources:**
- [Hugging Face Agents Course](https://huggingface.co/learn/agents-course) (same as above, listed here for sequencing)
- [Anthropic's own engineering blog and docs on building agents](https://docs.claude.com) — read the "building effective agents" and prompt engineering guides directly; this is the most current source on agent design patterns from the people building the models.
- [LangGraph / LangChain docs](https://langchain-ai.github.io/langgraph/) — for orchestration patterns (even if you end up not using the framework long-term, the patterns transfer).
- Karpathy's own framing is genuinely useful here: re-watch his ["Intro to Large Language Models"](https://karpathy.ai/) and any of his 2024–2025 conference talks on "the rise of agents" and what he calls the emerging OS-like role of LLMs — he's been unusually clear about this mental model.
- [rasbt/mini-coding-agent (GitHub)](https://github.com/rasbt/mini-coding-agent) — minimal, readable coding-agent harness; same "from scratch" philosophy applied to agents instead of models. Excellent for understanding what's *actually* happening under tools like Claude Code/Cursor instead of treating them as black boxes.

**What to build:**
- Build a minimal coding agent yourself (tool calling, loop, memory) before relying on a framework — same Karpathy philosophy applied one layer up the stack.
- Design and ship one real agentic workflow for a problem you actually have (not a toy), with logging/evaluation of failures.

**Validate:**
- You can explain the difference between a prompt chain, a ReAct-style agent loop, and a multi-agent system — and when each is actually appropriate vs. overkill.
- You can debug an agent that's looping/failing by reading its trace, not just by re-prompting and hoping.

---

## 10. Phase 7 — Deployment and MLOps for AI systems

**Resources:**
- [vLLM](https://docs.vllm.ai/) and [Ollama](https://ollama.com/) — local/self-hosted serving.
- [Hugging Face Inference Endpoints / Spaces](https://huggingface.co/docs/inference-endpoints/index) — the path the codewithdark-git repo itself uses for its Week 4 deployment step (Gradio + HF Hub).
- [LitGPT serving guide (Lightning AI)](https://lightning.ai/lightning-ai/studios/litgpt-serve) — directly referenced in Raschka's slides as the "private API" deployment pattern.
- Standard SRE/MLOps concepts: monitoring, latency/cost tradeoffs, batching, caching, fallback model routing — these matter as much as the model itself in production.

**Validate:**
- Take one of your finetuned/pretrained models and actually deploy it behind an API + simple UI (Gradio or otherwise), end to end, like the codewithdark-git repo's Week 4.

---

## 11. Phase 8 — Specialize (pick a lane)

By this point you have full-stack literacy. Now go deep in one direction:

| Track | What it looks like | Where to go next |
|---|---|---|
| **Research / pretraining** | Architecture, scaling laws, data curation | Read recent arXiv papers (cs.CL, cs.LG), reproduce results, contribute to open repos like nanochat |
| **Applied ML / finetuning** | Domain-specific models, RAG, evaluation | Go deep on PEFT, RAG architectures, eval-driven development |
| **Agents / applied AI engineering** | Production agent systems, tool use, orchestration | Go deep on Phase 6, contribute to agent frameworks, build real products |
| **Infra / systems** | Training/serving at scale, CUDA, distributed training | `llm.c`, CUDA programming, distributed training (FSDP, DeepSpeed) |
| **Alignment / safety** | RLHF, interpretability, evals for harm | Anthropic/OpenAI alignment research blogs, interpretability papers |

Given your background (developer, already using agents), **Applied AI Engineering / Agents** is the most natural near-term specialization with the fastest path to paid work, while **Research/pretraining** is the highest ceiling if you want to go where Karpathy actually went.

---

## 12. How to validate your knowledge (the part people skip)

A roadmap without checkpoints is just a reading list. Use these explicitly:

1. **Self-test materials that already exist:**
   - Raschka's free 170-page quiz PDF (per-chapter, ~30 questions each) — the single best "did I actually learn this" tool in this whole list.
   - lm-evaluation-harness — run real benchmarks against your own trained models instead of trusting your gut.

2. **Use LLMs (Claude, NotebookLM, etc.) as active examiners, not passive readers:**
   - **NotebookLM**: upload the Raschka PDF slides, the papers (Attention Is All You Need, etc.), and your own notes as sources. Use its "audio overview" and Q&A grounded-in-sources mode to quiz yourself — its strength is that it *won't* hallucinate beyond what you fed it, so it's a good fidelity check on the source material specifically.
   - **Claude (or any strong LLM)**: prompt it explicitly like — *"Act as a PhD-level oral exam committee on transformers/attention. Ask me progressively harder questions, don't accept hand-wavy answers, push back when I'm vague, and tell me directly when I'm wrong."* This is far more effective than "explain X to me" because it forces retrieval, not recognition.
   - Have an LLM **review your from-scratch code** against the reference implementation and explain *why* any deviation matters (not just that it differs).

3. **Build artifacts you can point to (the real proof):**
   - A from-scratch GPT you trained and can explain line by line.
   - A model you finetuned with LoRA + measured before/after on a real benchmark.
   - A deployed model/agent with a public demo link (HF Spaces is free and easy).
   - A speedrun leaderboard entry or comparable public benchmark submission.

4. **External validation (when ready):**
   - Submit to nanochat's community speedrun leaderboard.
   - Write up what you built (a blog post or repo README) — explaining it publicly is itself a comprehension test, and it's also literally how you get noticed for jobs in this space.
   - Contribute a small PR/fix to one of these open repos (rasbt's repos and nanochat both have active discussion boards).

---

## 13. Suggested pacing (flexible — go by mastery, not calendar)

- **Weeks 1–2:** Phase 0 + start Phase 1 (micrograd/makemore)
- **Weeks 3–5:** Finish Phase 1, do Phase 2 (nanoGPT + Raschka book chapters 2–4)
- **Weeks 6–8:** Phase 3 (run nanochat speedrun, get a real trained model talking)
- **Weeks 9–11:** Phase 4 (finetuning, DPO, dip into reasoning-from-scratch)
- **Weeks 12–14:** Phase 5 (HF ecosystem, eval harness, quantization) — run the **PyTorch for Deep Learning Professional Certificate** in parallel with this phase if you want the structured-course version alongside the from-scratch work
- **Weeks 15–17:** Phase 6 (agents — your strength, but go deeper than tool-usage)
- **Week 18+:** Phase 7 deployment, then pick Phase 8 specialization and go deep indefinitely

This is realistic for someone coding daily at ~10-15 focused hours/week. Compress if you can go full-time.

---

## 14. Master resource list (flat, for quick reference)

**People/Channels:**
- [Andrej Karpathy — YouTube](https://www.youtube.com/@AndrejKarpathy)
- [karpathy.ai](https://karpathy.ai/) (personal site, talks, Zero to Hero)
- [Sebastian Raschka — Substack](https://magazine.sebastianraschka.com/)
- [Jay Alammar — Illustrated guides](https://jalammar.github.io/)

**Repos:**
- [karpathy/micrograd](https://github.com/karpathy/micrograd)
- [karpathy/makemore](https://github.com/karpathy/makemore)
- [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- [karpathy/nanochat](https://github.com/karpathy/nanochat)
- [karpathy/llm.c](https://github.com/karpathy/llm.c)
- [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)
- [rasbt/reasoning-from-scratch](https://github.com/rasbt/reasoning-from-scratch)
- [rasbt/mini-coding-agent](https://github.com/rasbt/mini-coding-agent)
- [codewithdark-git/Building-LLMs-from-scratch](https://github.com/codewithdark-git/Building-LLMs-from-scratch) *(your original link — a study-planner layer on top of Raschka's book)*
- [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [Lightning-AI/litgpt](https://github.com/Lightning-AI/litgpt)

**Courses/Docs:**
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course)
- [Hugging Face Agents Course](https://huggingface.co/learn/agents-course)
- [CS231n (Stanford)](http://cs231n.stanford.edu/)
- [Anthropic Docs — prompt engineering & building agents](https://docs.claude.com)
- [vLLM Docs](https://docs.vllm.ai/)
- [PEFT Docs](https://huggingface.co/docs/peft/index)
- [Andrew Ng — Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction) *(concepts/math foundation, framework-agnostic value)*
- [PyTorch for Deep Learning Professional Certificate (DeepLearning.AI)](https://www.deeplearning.ai/courses/pytorch-for-deep-learning-professional-certificate) *(the current PyTorch-native equivalent of Ng's old TF-based Deep Learning Specialization)*
- [Transformers in Practice (DeepLearning.AI, Sharon Zhou)](https://www.deeplearning.ai/courses/transformers-in-practice)
- [Fine-tuning & RL for LLMs: Intro to Post-training (DeepLearning.AI, Sharon Zhou)](https://www.deeplearning.ai/courses/fine-tuning-and-reinforcement-learning-for-llms-intro-to-post-training)
- [How Transformer LLMs Work (DeepLearning.AI)](https://www.deeplearning.ai/courses/how-transformer-llms-work)

**Papers:**
- [Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762)
- [Language Models are Few-Shot Learners / GPT-3 (2020)](https://arxiv.org/abs/2005.14165)
- [LLaMA (2023)](https://arxiv.org/abs/2302.13971) / [Llama 2 (2023)](https://arxiv.org/abs/2307.09288)

**Books (the ones you found, confirmed current):**
- *Build a Large Language Model (From Scratch)* — Sebastian Raschka, Manning, 2024 — [book page](https://www.manning.com/books/build-a-large-language-model-from-scratch) | [slides PDF](https://sebastianraschka.com/pdf/slides/2024-build-llms.pdf)
- *Build A Reasoning Model (From Scratch)* — Sebastian Raschka, Manning, 2025 — [repo](https://github.com/rasbt/reasoning-from-scratch)

**Validation tools:**
- NotebookLM (notebooklm.google.com) — source-grounded Q&A/quizzing from your uploaded papers/slides
- Claude / any frontier LLM as an active oral-exam partner
- Raschka's free 170-page self-test PDF (linked from the Manning book page)
- lm-evaluation-harness, AlpacaEval, LMSYS Chatbot Arena for benchmarking your own models

---

*One last note from the "advisor" seat: don't let the from-scratch phases (1–4) take longer than ~2 months total. The risk for a working developer is perfectionism in the fundamentals and never reaching Phase 6 where your existing strengths compound fastest. Get competent, not perfect, on the internals — then spend real time where you already have an unfair advantage: agents and applied workflows.*
