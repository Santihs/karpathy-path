---
tags: [phase-6, agents, tool-use, orchestration]
status: not_started
---

# Phase 6 — Agents & Applied AI Workflows

> **Goal:** Turn "user of agent tools" into "person who understands and designs agent systems."
> This is your natural strength — go deep here, don't just stay at the surface.

## What to nail

- [[ReAct-Agent-Loop]] — reason + act loop, how it differs from a prompt chain
- [[Tool-Calling-Mechanics]] — function calling under the hood, structured output
- [[Prompt-Chaining-vs-Agents-vs-MultiAgent]] — when each is actually appropriate vs. overkill
- [[Agent-Memory-Patterns]] — in-context, external retrieval, procedural
- [[Mini-Coding-Agent-From-Scratch]] — build the loop yourself before using a framework

## Resources

1. [rasbt/mini-coding-agent (GitHub)](https://github.com/rasbt/mini-coding-agent) — minimal coding-agent harness; same from-scratch philosophy applied one layer up
2. [HuggingFace Agents Course](https://huggingface.co/learn/agents-course)
3. [Anthropic docs — building effective agents](https://docs.claude.com) — design patterns from people building the models
4. [LangGraph docs](https://langchain-ai.github.io/langgraph/) — orchestration patterns (understand the patterns; evaluate the framework separately)
5. Karpathy talks (2024–2025) — his "OS-like role of LLMs" mental model for agents

## What to build

- Minimal coding agent yourself: tool calling + loop + memory — before any framework
- One real agentic workflow for a problem you actually have, with logging/evaluation of failures
- Read the source of Claude Code or Cursor as a black-box exercise: what is it doing that you can now explain?

## Validation checkpoint

- Explain the difference between a prompt chain, ReAct-style agent loop, and a multi-agent system — and when each is appropriate vs. overkill
- Debug an agent that's looping/failing by reading its trace, not by re-prompting and hoping

## Links to topic notes

- [[ReAct-Agent-Loop]]
- [[Tool-Calling-Mechanics]]
- [[Prompt-Chaining-vs-Agents-vs-MultiAgent]]
- [[Agent-Memory-Patterns]]
- [[Mini-Coding-Agent-From-Scratch]]
