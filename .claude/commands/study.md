Read /00-Meta/progress.json to get my current state. Check today's day of week and determine the session type (weekday-micro / saturday-deep / sunday-deep-review / biweekly-cumulative — check last_cumulative_review for the biweekly trigger).

Scan flashcard-style files in /04-Quiz-Bank/ for `<!-- srs: ... due=YYYY-MM-DD ... -->` lines (missing = due today). Count how many have `due <= today`.

Then immediately output the briefing:
```
Phase X · [Phase Name] | Week N | [session type]
Current topic: [next_up value]
Today: [concrete plan for the next N minutes]
Due for review: N questions (run /quiz-me)
```

Then begin the session according to the rules in CLAUDE.md — don't wait for me to ask what to do.
