---
name: session-close
description: Close a karpathy-path study session — update progress.json, write the daily log, commit all vault changes with the [@Santihs] format, and push to main. Trigger whenever the user says "close session", "end session", "wrap up", "session done", "commit and push", "/session-close", or anything indicating they're done studying for the day.
---

# session-close

Follow every step below in order. Do not skip or ask for permission between steps — except at the two explicit confirmation gates marked **WAIT**.

---

## Step 1 — Load rules

Read `00-Meta/session-close-rules.md` if it exists and apply any custom preferences.
If it doesn't exist, continue with the defaults defined in this skill.

---

## Step 2 — Collect session inputs

Ask both questions in a single message:

1. **How long was the session?** (e.g. "25 min", "1.5h")
2. **Confirm status changes** — infer from the conversation what was covered and propose transitions:
   - Topics touched → `in_progress` (if they were `not_started`)
   - Topics where the user showed solid understanding → `done_needs_review`
   - Topics the user explicitly finished → `mastered`

   Example output:
   ```
   Proposed changes:
   - pytorch_tensors_autograd: not_started → in_progress
   - linear_algebra_vectors_matrices: not_started → in_progress
   Confirm? (yes / adjust)
   ```

**WAIT** for the user's response before continuing.

---

## Step 3 — Update progress.json

Read `00-Meta/progress.json`. Apply all confirmed changes:

- Status transitions confirmed in Step 2
- `total_hours_logged` += session duration (decimal hours — 25 min = 0.42)
- `study_streak`: if `last_session_date` was yesterday → increment; if today → keep; otherwise → reset to 1
- `last_session_date` = today (YYYY-MM-DD)
- `last_session_type` = session type based on today's day of week (weekday-micro / saturday-deep / sunday-deep-review)
- `session_count` += 1
- `next_up` = the specific next action (name the exact resource, chapter, or task — never vague like "continue")
- If today is ≥14 days after `last_cumulative_review` (or it's null), set a note to flag this at the next session start

Write the updated file.

---

## Step 4 — Write the session log

Write `/03-Daily-Logs/YYYY-MM-DD.md` (today's date) using the template at `00-Meta/daily-log-template.md`.

Fill in every section:
- `date`, `session_type`, `time_spent_minutes`
- `topics_touched` — all concepts and resources used
- `what_clicked` — genuine understanding moments from the conversation
- `what_I_struggled_with` — honest gaps or confusions that surfaced
- `quiz_results` — if quizzes happened, score them; otherwise N/A
- `resources_used` — all links, chapters, repos touched
- `what's_next` — copy `next_up` from progress.json verbatim
- `notes_for_vault` — anything still needing a `/02-Topics/` note or `/06-Doubts-Resolved/` entry

If a log for today already exists, append a second session block — do not overwrite.

---

## Step 5 — Confirmation gate before commit

Run `git diff --stat HEAD` to show what changed. Then propose the full commit command:

```
[@Santihs]: <type>: <description>
```

**Type rules:**
- `study:` — new material covered
- `review:` — quiz or spaced-repetition session
- `chore:` — vault structure, template, or config changes only

**Description rules:**
- Keep the subject line direct and specific — name the phase and main concept(s)
- No filler, no "session notes", no padding
- Only add a commit body (blank line + extra lines) when the session touched many distinct things that each warrant attention — if one clear subject line covers everything, stop there
- Never add `Co-Authored-By` or any trailer lines

Good (subject only):
- `[@Santihs]: study: Phase 0 — PyTorch tensors + autograd blitz (Week 1)`
- `[@Santihs]: review: Phase 0 quiz — linear algebra + gradients`

Good (with body, only when warranted):
```
[@Santihs]: study: Phase 0 — linear algebra + calculus + PyTorch blitz

- Completed 3B1B linear algebra series (ch 1-5)
- Ran PyTorch 60-min blitz end to end
- Identified gap: chain rule still shaky
```

Bad:
- `[@Santihs]: study: session notes`
- `[@Santihs]: study: progress update`
- Any message with a `Co-Authored-By:` trailer

Show the user exactly what will run:
```bash
git add -A && git commit -m "[@Santihs]: study: ..."
git push origin main
```

**WAIT** for confirmation or edits before running anything.

---

## Step 6 — Commit and push

Run:
```bash
git add -A
git commit -m "<confirmed message>"
git push origin main
```

Report: commit hash, files changed, push status.
If push fails, report the error and suggest the fix (`git remote add origin <url>` or `--set-upstream`).

---

## Step 7 — Close summary

Print this block and nothing else:

```
Session closed
─────────────────────────────
Date:         YYYY-MM-DD
Duration:     N min
Streak:       N days
Total hours:  N.Nh
Phase:        X · [name]
Next up:      [next_up value]
─────────────────────────────
```
