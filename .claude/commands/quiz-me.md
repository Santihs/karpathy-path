# /quiz-me — Retrieval practice round (FSRS-lite + generation-first)

Read `00-Meta/progress.json` for phase/topic context. Read all flashcard-style
files in `04-Quiz-Bank/` (plain `Q:` / `A:` pairs — skip exercise-sheet files
that have no `Q:` lines, e.g. worked-problem sets). This covers the frozen
archive files; for the live `04-Quiz-Bank/karpathy/` deck (one file per card,
synced to Anki) apply the same due-date/interleaving/self-explain logic below
using each card's own review history in Anki instead of an `srs:` comment —
if asked to quiz from that folder, just walk the cards themselves since Anki
owns scheduling there.

1. For each `Q:`/`A:` pair, parse the trailing
   `<!-- srs: ease=X interval=Y due=YYYY-MM-DD lapses=Z last_seen=W -->`
   comment. No `srs:` line = never seen = `due=today`, top priority.

2. **Select questions, interleaved by topic**: build the due pool (`due <=
   today`), most-overdue first within each topic as the priority signal.
   Then group the pool by primary topic tag (first non-`phase-N` tag) and
   round-robin across groups when filling the round — no two consecutive
   questions should share a primary topic tag, unless fewer than 2 distinct
   topics are due (then just go most-overdue-first, interleaving isn't
   possible with one topic). Prefer topics where `progress.json` confidence
   < 3 or `last_tested` is oldest when there's a tie within a group. Cap at 5
   per round. If nothing is due, tell the user what's coming up next
   (soonest `due`) instead of quizzing.

3. **Generation-first, one question at a time:**
   - Show ONLY the `Q:`. No hints, no partial answer.
   - **If the card has `self-explain: true`** in its frontmatter (or is
     tagged as such): explicitly ask for a full explanation in their own
     words first — "explicá esto con tus propias palabras, como si me lo
     tuvieras que enseñar a mí" — before grading, not just "answer the
     question." These are the densest derivation/threshold-concept cards;
     don't let a terse correct-sounding answer pass as equivalent to a full
     explanation.
   - Wait for the user's answer before revealing `A:`.

4. **Grade strictly** after they answer — correct / partial / incorrect.
   Partial = gets the gist but misses a specific detail or qualifier; don't
   round up to correct. Show the stored `A:` and a one-sentence explanation
   if they missed something. **For `self-explain` cards**, also point them
   to the card's `Ref:` line (topic-note section or source file) for the
   full derivation — the stored `A:` is intentionally terse, comparing
   against it alone isn't enough for these.

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
