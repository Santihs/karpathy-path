# Study Notifier — Setup Guide

Sends a daily email + Google Calendar event at 6pm Bolivia time based on your `progress.json`.
Runs on GitHub Actions — no server, no local daemon, free for public repos.

---

## One-time setup (~10 min)

### 1. Gmail App Password

1. Go to [myaccount.google.com](https://myaccount.google.com) → **Security**
2. Enable **2-Step Verification** if not already on
3. Search for **App Passwords** (or go to Security → App Passwords)
4. Create one: App = **Mail**, Device = **Other** → name it "karpathy-notifier"
5. Copy the 16-character password — you'll need it in step 4

---

### 2. Google Cloud — Enable Calendar API

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (name it anything, e.g. `karpathy-notifier`)
3. Go to **APIs & Services → Library** → search **Google Calendar API** → Enable
4. Go to **APIs & Services → Credentials** → **Create Credentials → OAuth 2.0 Client ID**
5. Application type: **Desktop app** → name it anything → Create
6. Download the JSON → save it as `notifier/credentials.json` in this repo (it is gitignored)

---

### 3. Run the auth script once (gets your Calendar token)

Make sure `uv` is installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`), then:

```bash
uv run notifier/auth.py
```

A browser window will open → log in to Google → grant Calendar access.
The script prints a JSON block. Copy the **entire JSON** — you'll paste it into a GitHub Secret next.

---

### 4. Add secrets to GitHub

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret name | Value |
|---|---|
| `GMAIL_ADDRESS` | `your-gmail@gmail.com` |
| `GMAIL_APP_PASSWORD` | The 16-char password from step 1 |
| `GCAL_TOKEN_JSON` | The full JSON block printed by `auth.py` in step 3 |
| `GCAL_CALENDAR_ID` | `primary` (unless you want a specific calendar) |

---

### 5. Test it

**Local test** (requires a `notifier/.env` file — see below):
```bash
# Create notifier/.env with:
# GMAIL_ADDRESS=your-gmail@gmail.com
# GMAIL_APP_PASSWORD=your-app-password
# GCAL_TOKEN_JSON={"token": "...", ...}
# GCAL_CALENDAR_ID=primary

uv run notifier/remind.py
```

**GitHub Actions test** (uses the real secrets):
1. Go to repo → **Actions → Study Reminder → Run workflow**
2. Check your email and Google Calendar

---

## How it works

- Runs every day at **22:00 UTC (6pm Bolivia)**
- Reads `progress.json` directly from the public GitHub repo
- Determines tomorrow's session type (weekday-micro / saturday-deep / sunday-deep-review)
- Flags biweekly cumulative review if overdue (≥14 days)
- Sends email with session brief + streak warning if you missed today
- Creates a Google Calendar event at **9am tomorrow** (block length depends on session type)

---

## Gitignored files (never commit these)

```
notifier/credentials.json   ← Google OAuth client secret
notifier/token.json         ← your personal access token
notifier/.env               ← local test env vars
```
