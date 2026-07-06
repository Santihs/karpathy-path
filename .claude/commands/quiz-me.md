# /quiz-me — Retrieval practice round (FSRS-lite + generation-first)

Read `00-Meta/progress.json` for phase/topic context. Read all flashcard-style
files in `04-Quiz-Bank/` (plain `Q:` / `A:` pairs — skip exercise-sheet files
that have no `Q:` lines, e.g. worked-problem sets).

1. For each `Q:`/`A:` pair, parse the trailing
   `<!-- srs: ease=X interval=Y due=YYYY-MM-DD lapses=Z last_seen=W -->`
   comment. No `srs:` line = never seen = `due=today`, top priority.

2. Select questions where `due <= today`, most-overdue first. Prefer topics
   where `progress.json` confidence < 3 or `last_tested` is oldest when
   there's a tie. Cap at 5 per round. If nothing is due, tell the user what's
   coming up next (soonest `due`) instead of quizzing.

3. **Generation-first, one question at a time:**
   - Show ONLY the `Q:`. No hints, no partial answer.
   - Wait for the user's answer before revealing `A:`.

4. **Grade strictly** after they answer — correct / partial / incorrect.
   Partial = gets the gist but misses a specific detail or qualifier; don't
   round up to correct. Show the stored `A:` and a one-sentence explanation
   if they missed something.

5. **Update scheduling** for that question's `srs:` line right after grading
   (SM-2 simplified), write it back into the file immediately:
   - Correct → `interval = round(interval * ease)`, `ease = min(3.0, ease + 0.1)`
   - Partial → `interval = max(1, round(interval * 0.5))`, ease unchanged
   - Incorrect → `interval = 1`, `ease = max(1.3, ease - 0.2)`, `lapses += 1`
   - `due = today + interval days`, `last_seen = today`

6. At the end: give a score, flag topics that need review (based on
   incorrect/partial answers), and show the next 1-2 upcoming `due` dates.

7. Update `last_tested` dates in the relevant quiz bank file frontmatter and
   note weak spots in the relevant `/02-Topics/` notes — same as before.
