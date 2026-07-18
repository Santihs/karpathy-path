---
name: note-collect
description: Collect photos, screenshots, definitions, and explanations pasted during a karpathy-path study session into a running scratch buffer, then compile them into a permanent /02-Topics/ note on command. Use this whenever the user pastes a local image/screenshot path during a session, types a short definition or their own explanation and says to save/note it (e.g. "anota esto", "guardá esto", "recopila esto"), or asks to compile everything collected so far into a note (e.g. "escribí todo", "compilá la nota", "armá la nota", "write it down"). Do NOT use for closing out a full session (that's session-close) or for quiz/spaced-repetition (that's quiz-me) — this skill only touches scratch buffer + /02-Topics/ + /07-Visuals/ + /06-Doubts-Resolved/.
---

# note-collect

Two phases: **collect** (runs continuously through the session, cheap, no vault writes) and **compile** (runs once, on request, writes to the vault). Never skip straight to compiling from memory alone — the whole point of collecting is that nothing gets lost between the moment something is pasted and the moment the note gets written.

---

## Phase 1 — Collect

Triggered any time during the session the user pastes a local file path (photo, screenshot) or types something worth keeping (a definition, their own explanation, a correction to something you said) and flags it as worth saving — "anota esto", "guardá esto", "recopila esto", or just an implicit "guardá esa foto"/"guardá esa idea".

For each item:

1. **If it's a local image/screenshot path**: read it immediately with the Read tool (it handles images directly) — don't wait until compile time to look at it, the path or file might not be around later. Write a short description of what's in the image to the buffer, plus the path itself.
2. **If it's text** (a definition the user typed, a correction, a "wait so X means Y?" moment): append it to the buffer verbatim, tagged with who said it.
3. **If it's one of your own explanations from earlier in this conversation** that the user flags as worth keeping ("esa explicación guardala"): pull the relevant part of your own prior response and append it.

Append each item to a single scratch file for the session:
`<scratchpad>/note-collect-buffer.md` (the scratchpad path is given in your system prompt — reuse it, don't invent a new temp location).

Format each entry as:
```
## [HH:MM or sequence order] <fuente: usuario | claude | imagen>
<contenido o descripción de la imagen + path>
```

Confirm collection tersely ("guardado") and get straight back to whatever the study session was doing — this phase must not interrupt the flow of the lesson. No web research, no vault writes, no frontmatter decisions happen here.

If the buffer file doesn't exist yet, create it. If it exists, append — never overwrite mid-session.

---

## Phase 2 — Compile

Triggered by "escribí todo", "compilá la nota", "armá la nota", or equivalent. This is the only phase that writes to the vault, so it's more deliberate.

### Step 1 — Read the buffer

Read `<scratchpad>/note-collect-buffer.md`. If it's empty or missing, say so and stop — nothing to compile.

### Step 2 — Figure out where this goes

Check `00-Meta/progress.json` for `next_up` and the current phase/topic to infer `phase-N` and a sensible topic tag. Check `02-Topics/` for an existing note this content belongs to (same topic already has a file → append a new section there rather than creating a duplicate note).

If it's genuinely ambiguous which topic or which file (new vs. existing), ask — one short question, don't guess on something that determines the file's identity for the rest of the vault's life.

### Step 3 — Verify and enrich with web research

This vault's rule for doubt resolution applies here too: don't write concept explanations from memory alone. For anything in the buffer that's a concept (not just raw data like "photo of my whiteboard sketch"), search the web and verify against authoritative sources — official docs, the original paper, Raschka's materials, Hugging Face docs, Anthropic docs. Where it helps the learning, look for how the concept shows up in a real ML/AI project or implementation (a real repo, a real paper's use of it) — a concrete example lands better than an abstract definition.

If this research resolves something the user was genuinely unsure about (not just background enrichment), write it as its own note in `06-Doubts-Resolved/[slug].md` following the existing format in that folder (frontmatter: `tags`, `date_resolved`; body: plain explanation + `## Fuentes` with inline links), and link it from the `02-Topics/` note under a `## Doubts Resolved` section — this matches the cross-linking CLAUDE.md already requires.

Cite sources inline in the note, not just as a bare link dump.

### Step 4 — Build any visuals

If a matrix table, a formula with subscripts, or anything else the chat can't render cleanly needs a diagram, reuse what's already in this repo — do not invent a new visual system:
- Template: `07-Visuals/_template.html`
- Generator: `07-Visuals/viz_html.py` (see `07-Visuals/viz_examples.py` for usage patterns)

Output file: `07-Visuals/<topic>-<YYYY-MM-DD>.html`. Link it from the compiled note.

### Step 5 — Draft the note

Write in Spanish. Math inside the note file can use LaTeX (Obsidian renders it) — this restriction only applies to the chat, not the file. Follow the vault's frontmatter convention exactly:

```yaml
---
tags: [phase-N, topic-tag]
status: seed | learning | solid
first_learned: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
confidence: N/5
---
```

- New note → `first_learned` = today, `status` = `seed` unless the buffer shows real depth (then `learning`).
- Existing note being appended to → update `last_reviewed` = today, bump `confidence` only if the session content shows the user actually leveled up (don't inflate it by default).
- Body: organize by what's actually in the buffer — don't force a rigid template on content that doesn't fit it. Reference images by their original path (or copy them into an `assets/` location next to the note if the vault has one — check before inventing a new convention).
- Cross-link any `07-Visuals/*.html` and any `06-Doubts-Resolved/*.md` created in Steps 3-4.

### Step 6 — WAIT gate

Show the user the drafted note content (or a diff if appending to an existing file) before writing it. Wait for confirmation or edits — this is the one irreversible step (a vault file that'll get committed later), so don't skip the check the way Phase 1 does.

### Step 7 — Write and clean up

Once confirmed:
1. Write the `02-Topics/` note (new file or append).
2. Write any `06-Doubts-Resolved/` and `07-Visuals/` files from Steps 3-4.
3. Clear the scratch buffer (`<scratchpad>/note-collect-buffer.md`) — the material now lives permanently in the vault, no reason to keep the temp copy.

**Out of scope, on purpose:** this skill never touches `00-Meta/progress.json` or `04-Quiz-Bank/` — that's `session-close`'s and `quiz-me`'s job respectively. Don't update streaks, hours, or generate quiz questions here even if it'd be convenient; keep this skill scoped to notes only so it doesn't collide with what those skills own.

### Step 8 — Confirm

One line: what got written, where, and what's still pending (e.g. "nota actualizada en 02-Topics/X.md, 1 doubt resuelto, 1 visual generado — buffer limpio").
