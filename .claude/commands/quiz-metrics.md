# /quiz-metrics — Topic mastery snapshot from Anki review data

Anki desktop must be running (AnkiConnect on localhost:8765). Run this exact command:

```
uv run --project anki-metrics python anki-metrics/metrics.py --dir 04-Quiz-Bank/karpathy --repo karpathy --out 00-Meta/quiz-metrics/$(date +%F).md
```

If it errors with a connection failure, tell me to open Anki desktop first.

Once it succeeds, read the generated report file back and summarize in chat:
- List every topic with verdict `needs-repass` first, explicitly.
- One line naming the `solid` topics.
- Mention `developing` topics only if I ask.

Then stage and commit the report file with a plain descriptive commit message (e.g. `study: quiz metrics snapshot YYYY-MM-DD`). Don't push automatically — mention I can push manually.
