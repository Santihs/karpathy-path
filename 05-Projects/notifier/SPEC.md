# Study Notifier — Spec

## Purpose

A daily automated reminder that fires at **6pm Bolivia time (UTC-4)** every day.
It reads `progress.json` from the GitHub repo, computes tomorrow's session brief,
sends an email, and creates a Google Calendar event for the study block.

No server. No local daemon. Runs free on GitHub Actions.

---

## Behavior

### Trigger
- GitHub Actions cron: `0 22 * * *` (22:00 UTC = 6pm Bolivia)
- Also triggerable manually via `workflow_dispatch` for testing

### Inputs
Fetched from raw GitHub URL (public repo, no auth):
```
https://raw.githubusercontent.com/Santihs/karpathy-path/main/00-Meta/progress.json
```

Fields used:
| Field | Use |
|---|---|
| `meta.last_session_date` | Detect missed sessions (streak risk) |
| `meta.study_streak` | Show in email subject |
| `meta.current_phase` | Show phase in email + calendar title |
| `meta.current_week` | Show week in email |
| `meta.next_up` | The concrete next action |
| `meta.total_hours_logged` | Stats footer |
| `meta.session_count` | Stats footer |
| `meta.last_cumulative_review` | Flag biweekly review if overdue |

### Session Type Logic (based on tomorrow's day of week)
| Tomorrow           | Session type          | Calendar block                                                  |
| ------------------ | --------------------- | --------------------------------------------------------------- |
| Mon–Fri            | `weekday-micro`       | 30 min                                                          |
| Saturday           | `saturday-deep`       | 3 hours                                                         |
| Sunday             | `sunday-deep-review`  | 2 hours                                                         |
| Any day (override) | `biweekly-cumulative` | 1.5 hours — if `last_cumulative_review` is null or ≥14 days ago |

### Email Output
```
Subject: Study tomorrow — Phase N · Week N [streak: Nd]

Session type: weekday-micro (30 min)
Next up: [next_up value from progress.json]

Total hours: N.Nh | Sessions: N
```

If session was missed today (last_session_date < today):
```
⚠ Streak at risk — no session logged today. Don't break the chain.
```

If biweekly review is overdue:
```
📋 Biweekly cumulative review overdue — focus on spaced recall, not new content.
```

### Google Calendar Event
- **Title**: `Study — weekday-micro · Phase N`
- **Date**: tomorrow
- **Time**: 9:00am–9:30am (weekday) / 9:00am–12:00pm (Saturday) / 9:00am–11:00am (Sunday)
- **Description**: value of `next_up`
- **Color**: blue (blueberry)
- **Reminder**: 10 min before (popup)

---

## Stack

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.12 | stdlib email/smtplib, standard Google SDK, ML ecosystem |
| Deps management | `uv` + `pyproject.toml` + `uv.lock` | Reproducible installs, lockfile committed, no pip |
| Email transport | Gmail SMTP (port 587, STARTTLS) | App Password — no OAuth dance for email |
| Calendar | Google Calendar API v3 | OAuth2 with refresh token stored as GitHub Secret |
| CI/CD | GitHub Actions | Free for public repos, no server needed |

---

## File Layout

```
karpathy-path/
├── .github/
│   └── workflows/
│       └── study-reminder.yml     ← cron + manual trigger
├── notifier/
│   ├── pyproject.toml             ← uv project definition + deps
│   ├── uv.lock                    ← committed lockfile (reproducible CI)
│   ├── remind.py                  ← main script
│   ├── auth.py                    ← one-time local OAuth helper
│   └── README.md                  ← setup guide (secrets, Google Cloud, test)
```

Gitignored (never commit):
```
notifier/credentials.json   ← Google OAuth client secret
notifier/token.json         ← local token (only needed during auth setup)
notifier/.env               ← local test env vars
notifier/.venv              ← uv virtual environment
```

Local dev workflow:
```bash
cd notifier
uv sync          # install deps into .venv
uv run remind.py # run with vars from .env
```

---

## Secrets (added once to GitHub repo → Settings → Secrets)

| Secret | Value | How to get |
|---|---|---|
| `GMAIL_ADDRESS` | `sanchezx1601@gmail.com` | Already known |
| `GMAIL_APP_PASSWORD` | 16-char token | Google Account → Security → 2-Step → App Passwords → Mail |
| `GCAL_TOKEN_JSON` | Token JSON with refresh_token | Run `uv run auth.py` once locally, copy printed JSON |
| `GCAL_CALENDAR_ID` | `primary` (or specific calendar ID) | Google Calendar settings → calendar ID |

---

## One-Time Setup Checklist

- [ ] Google Cloud: create project → enable Calendar API → create OAuth2 credentials (Desktop) → download `credentials.json` into `notifier/`
- [ ] Gmail: enable 2-Step Verification → generate App Password for Mail
- [ ] `cd notifier && uv sync` — install deps
- [ ] `uv run auth.py` — browser OAuth flow → copy printed JSON into `GCAL_TOKEN_JSON` secret
- [ ] Add all 4 secrets to GitHub repo Settings → Actions → Secrets
- [ ] Create `notifier/.env` with the 4 vars → `uv run remind.py` → confirm email + calendar event
- [ ] Trigger GitHub Action manually (`workflow_dispatch`) → confirm same
- [ ] First automated run: next 6pm Bolivia → confirm on phone

---

## Non-goals

- No AI/LLM in the script — pure data → message logic
- No local cron — GitHub Actions only
- No Slack/Discord — email + calendar is enough
- No tracking of whether the email was read
