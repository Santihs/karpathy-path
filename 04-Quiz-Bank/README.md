# Quiz Bank

Spaced-repetition Q&A pairs. Generated as concepts are learned and demonstrated solidly.

## Format

Each file in this folder is a set of questions tagged by phase and topic:

```yaml
---
tags: [phase-N, topic-slug]
date_added: YYYY-MM-DD
last_tested: null
---

Q: Question text here?
A: Answer text here.

---

Q: Next question?
A: Next answer.
```

## How this is used

- **Weekday micro-sessions**: Claude pulls 3–5 questions tagged to the most recent weekend's topics.
- **Biweekly cumulative**: Claude pulls questions from topics with `date_added` or `last_tested` older than 2 weeks.
- After testing, `last_tested` is updated and weak spots are flagged for re-explanation.

## Index

<!-- Entries added here as quiz files are created -->
