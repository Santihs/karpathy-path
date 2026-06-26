import json
import os
import smtplib
import urllib.request
from datetime import date, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

PROGRESS_URL = "https://raw.githubusercontent.com/Santihs/karpathy-path/main/00-Meta/progress.json"
TIMEZONE = "America/La_Paz"


def fetch_progress() -> dict:
    with urllib.request.urlopen(PROGRESS_URL) as r:
        return json.loads(r.read())


def session_type_for(day: date) -> tuple[str, int]:
    """Return (session_type, duration_minutes) for the given day."""
    dow = day.weekday()  # 0=Mon … 6=Sun
    if dow == 5:
        return "saturday-deep", 180
    if dow == 6:
        return "sunday-deep-review", 120
    return "weekday-micro", 30


def build_email(meta: dict, tomorrow: date, today: date | None = None) -> tuple[str, str, str, int]:
    if today is None:
        today = date.today()
    streak = meta.get("study_streak", 0)
    phase = meta.get("current_phase", 0)
    week = meta.get("current_week", 1)
    next_up = meta.get("next_up", "Check progress.json")
    total_hours = meta.get("total_hours_logged", 0)
    sessions = meta.get("session_count", 0)
    last_session = meta.get("last_session_date")
    last_cumulative = meta.get("last_cumulative_review")

    streak_at_risk = last_session and date.fromisoformat(last_session) < today

    biweekly_overdue = last_cumulative is None or (
        today - date.fromisoformat(last_cumulative)
    ).days >= 14

    session_type, duration = session_type_for(tomorrow)
    if biweekly_overdue:
        session_type = "biweekly-cumulative"
        duration = 90

    subject = f"Study tomorrow — Phase {phase} · Week {week} [streak: {streak}d]"

    lines = [
        f"Session type: {session_type} ({duration} min)",
        f"Next up: {next_up}",
        "",
    ]
    if streak_at_risk:
        lines.append("⚠ Streak at risk — no session logged today. Don't break the chain.")
    if biweekly_overdue:
        lines.append("📋 Biweekly review overdue — focus on spaced recall, not new content.")
    lines += [
        "",
        f"Total hours: {total_hours}h | Sessions: {sessions}",
    ]

    return subject, "\n".join(lines), session_type, duration


def send_email(subject: str, body: str) -> None:
    address = os.environ["GMAIL_ADDRESS"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart()
    msg["From"] = address
    msg["To"] = address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(address, password)
        smtp.send_message(msg)

    print(f"✓ Email sent: {subject}")


def create_calendar_event(
    day: date, session_type: str, next_up: str, duration_min: int, phase: int
) -> None:
    token_json = os.environ["GCAL_TOKEN_JSON"]
    calendar_id = os.environ.get("GCAL_CALENDAR_ID", "primary")

    creds = Credentials.from_authorized_user_info(json.loads(token_json))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    service = build("calendar", "v3", credentials=creds)

    start = datetime(day.year, day.month, day.day, 9, 0)
    end = start + timedelta(minutes=duration_min)

    event_id = f"srem{day.strftime('%Y%m%d')}"  # only [a-v0-9] allowed by Google Calendar API

    event = {
        "id": event_id,
        "summary": f"Study — {session_type} · Phase {phase}",
        "description": next_up,
        "start": {"dateTime": start.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end.isoformat(), "timeZone": TIMEZONE},
        "colorId": "7",  # Peacock (blue)
        "reminders": {
            "useDefault": False,
            "overrides": [{"method": "popup", "minutes": 10}],
        },
    }

    try:
        result = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"✓ Calendar event created: {result.get('htmlLink')}")
    except HttpError as e:
        if e.status_code == 409:  # already exists — update it
            result = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
            print(f"✓ Calendar event updated (already existed): {result.get('htmlLink')}")
        else:
            raise


def main() -> None:
    progress = fetch_progress()
    meta = progress["meta"]

    tomorrow = date.today() + timedelta(days=1)
    subject, body, session_type, duration = build_email(meta, tomorrow)

    send_email(subject, body)
    create_calendar_event(
        tomorrow,
        session_type,
        meta.get("next_up", ""),
        duration,
        meta.get("current_phase", 0),
    )


if __name__ == "__main__":
    main()
