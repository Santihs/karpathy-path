# Claude Code Bootstrap Prompt — AI Learning Tracker + Obsidian Brain

> **How to use this file:** Open a terminal in an empty folder (e.g. `~/ai-learning`), run `claude` to start Claude Code there, and paste everything in the box below as your first message. Attach `AI_Roadmap_From_Developer_to_Karpathy_Level.md` (the roadmap file from our earlier conversation) to that same message so Claude Code has the actual curriculum content to work from. Claude Code will then build the whole system in one pass and ask you anything it's missing.

---

## The prompt to paste into Claude Code

```
I'm attaching my AI learning roadmap (AI_Roadmap_From_Developer_to_Karpathy_Level.md).
I want you to set up a permanent system in this folder that does three things:
acts as an Obsidian vault (my second brain for this), tracks my real progress
through the roadmap as structured data, and gives you (Claude Code) a repeatable
"skill" for running my study sessions — so that every time I open this folder and
say something like "let's study" or "what's today's lesson", you already know
exactly what to do without me re-explaining context.

MY CONSTRAINTS (design the system around these, don't ask me to change them):
- Weekdays (Mon-Fri): 20-30 min/day, micro-sessions only. No new heavy concepts —
  retrieval practice (quiz me on the weekend's material) or one small forward step
  (one video chapter, one notebook cell, reading one section).
- Saturday: 2-4 hours, deep work — this is where new hands-on coding/training happens.
- Sunday: 1.5-3 hours — continue Saturday's thread, then END the session with a
  quiz/review round before the week resets.
- Every 2 weeks: a cumulative review session that quizzes me on material from
  2-3 weeks ago, not just the most recent weekend, to fight forgetting.
- I have a separate personal SaaS project — keep it COMPLETELY OUT of this vault
  and out of scheduling. This space is only for the AI/ML roadmap.
- I'm a working developer already using AI agents day to day, so don't waste time
  re-explaining things at a total-beginner level — calibrate explanations to that.

WHAT TO BUILD:

1. OBSIDIAN VAULT STRUCTURE
   Set up the folder as a valid Obsidian vault (create a .obsidian config folder
   is not necessary — Obsidian auto-detects any folder of markdown files, so just
   get the markdown structure and conventions right):

   /00-Meta/          -> the roadmap itself, the curriculum map, this system's own docs
   /01-Phases/        -> one note per roadmap phase (Phase 0 ... Phase 8), each phase
                          note links out to its own topic notes via [[wikilinks]]
   /02-Topics/        -> one atomic note per concept (e.g. "Backpropagation.md",
                          "Self-Attention.md", "LoRA.md") — these are the real
                          knowledge units, written in my own words after I learn them,
                          with frontmatter: tags, status (seed/learning/solid),
                          date-first-learned, date-last-reviewed, source links
   /03-Daily-Logs/     -> one note per study session, named YYYY-MM-DD.md, using a
                          consistent template (see below)
   /04-Quiz-Bank/      -> question/answer pairs generated as I go, tagged by topic,
                          used for spaced repetition later
   /05-Projects/       -> notes on hands-on builds (the nanoGPT clone, the nanochat
                          run, any finetuning experiment) — what I built, what broke,
                          what I learned debugging it
   /06-Doubts-Resolved/ -> see point 4 below — this is the "verified against the
                          internet" knowledge log

   Use frontmatter consistently, e.g.:
   ---
   tags: [phase-2, transformers, attention]
   status: learning
   first_learned: 2026-06-27
   last_reviewed: 2026-06-27
   confidence: 2/5
   ---

2. PROGRESS TRACKING AS DATA
   Create /00-Meta/progress.json as the single source of truth — structured, not
   prose, so it's easy for you (Claude Code) to read and update programmatically
   every session. Structure it around the roadmap's phases and give each topic
   a status: not_started | in_progress | done_needs_review | mastered.
   Also track: current phase, current week, last session date, study streak,
   total hours logged, and a "next_up" pointer so you always know what's next
   without me telling you.

3. THE DAILY SESSION SKILL (this is the most important part)
   Create a CLAUDE.md in the root of this folder (Claude Code reads this
   automatically on every session in this directory) that defines your standing
   instructions. It must specify:

   - On session start, ALWAYS read /00-Meta/progress.json first to know where
     I am, then check today's day-of-week to decide session type
     (weekday-micro / saturday-deep / sunday-deep-plus-review / biweekly-cumulative).
   - State clearly at the start of every session: what phase/topic we're in,
     what today's session type is, and what we're doing in the next N minutes —
     don't make me ask.
   - For weekday micro-sessions: default to quizzing me first on the most recent
     weekend's material (pull from /04-Quiz-Bank/ and /02-Topics/), THEN if time
     remains, advance one small step. Keep it tight — respect the 20-30 min budget,
     don't let a session balloon.
   - For weekend deep sessions: help me work through the actual roadmap content
     (reading, coding, running things), act as a Socratic explainer when I'm stuck
     (ask me what I think first before just telling me), and on Sunday close
     every session with a short quiz round and a session log written to
     /03-Daily-Logs/.
   - WHEN I HAVE A DOUBT OR QUESTION ABOUT A CONCEPT: don't just answer from
     memory. Use web search to verify the explanation against current,
     authoritative sources (official docs, the original paper, Sebastian
     Raschka's materials, Hugging Face docs, etc.) before answering, especially
     for anything that might have changed or where you're not fully certain.
     Then write the resolved explanation, with sources, into
     /06-Doubts-Resolved/ as a permanent note, and link it from the relevant
     topic note in /02-Topics/.
   - After ANY session, update /00-Meta/progress.json (status changes, streak,
     hours, next_up) and write/update the relevant /02-Topics/ notes — don't
     leave knowledge only in chat history, it has to land in the vault.
   - Maintain the quiz bank: every time I demonstrate I've learned something
     solidly, generate 2-3 quiz questions about it into /04-Quiz-Bank/, tagged
     by topic, for future spaced-repetition sessions.
   - Every 2 weeks, proactively flag that it's time for a cumulative review
     session and pull questions from topics tagged 2-3+ weeks old.
   - Keep the SaaS project entirely out of scope — if I mention it, treat it
     as off-topic for this vault.

4. A REPEATABLE SLASH COMMAND
   Set up a custom slash command (.claude/commands/study.md or equivalent
   convention for this Claude Code version) so I can just type /study and you
   immediately: read progress.json, announce today's session plan, and start.
   Also set up /quiz-me as a standalone command I can run anytime outside the
   normal flow for quick retrieval practice.

5. DAILY LOG TEMPLATE
   Create /00-Meta/daily-log-template.md with a consistent structure: date,
   session type, time spent, topics touched, what I struggled with, quiz
   results, what's next. Use this template every time you write to
   /03-Daily-Logs/.

After building all of this, give me a short summary of what you created, the
exact commands I'll use day to day, and ask me anything you need clarified
before we run our first real session.
```

---

## What this prompt makes Claude Code actually build

| Piece | Purpose |
|---|---|
| Obsidian-compatible folder structure | Your notes become a real knowledge graph — Obsidian's link/graph view shows how Attention connects to Transformers connects to nanoGPT, etc. No extra plugin needed; Claude Code just needs to write plain markdown with `[[wikilinks]]` and frontmatter correctly. |
| `progress.json` | Lets Claude Code answer "what's next" instantly without you re-explaining state every session — this is what makes the "I'm talking to an AI" reinforcement loop actually work mechanically. |
| `CLAUDE.md` | This is the actual *skill* — standing instructions Claude Code auto-loads every time you open this folder, so it behaves consistently without you re-prompting. |
| `/06-Doubts-Resolved/` | The "confirm against the internet" loop you asked for — Claude Code is explicitly told to verify against current sources before answering and to leave a permanent, sourced record instead of an answer that evaporates when the chat ends. |
| `/04-Quiz-Bank/` + `/quiz-me` command | The spaced-repetition / active-recall engine — this is the actual mechanism that fights forgetting, not just a tracker. |
| `/study` slash command | Removes all friction — you don't plan, you just type one command and Claude Code tells you what today's 20-30 min (or weekend block) consists of. |

---

## Why this design matches your constraints

- **Weekday 20-30 min** is *protected* by instructing Claude Code to quiz-first and cap scope — without this constraint stated explicitly, sessions drift long.
- **SaaS stays separate** by explicit exclusion in both the vault scope and the `CLAUDE.md` instructions — Claude Code won't conflate the two projects' context even if you mention the SaaS in passing.
- **"Talk to me like I'm an AI"** is literally what spaced repetition + active recall + a persistent state file *is* — you're building yourself a memory/retrieval system instead of relying on vague intent to "review sometime."
- **Obsidian as the brain** means none of this knowledge is trapped in a chat transcript — it's durable, searchable, linkable, and survives long after any individual Claude Code session ends.

---

## One small recommendation before you run this

Do this bootstrap on a **Saturday**, not a weekday — it'll take 15-20 minutes of back-and-forth with Claude Code to get the structure right and answer its clarifying questions, and that's a deep-work-block activity, not a 20-minute weekday slot.
