import json
import smtplib
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pytest
from googleapiclient.errors import HttpError

from remind import build_email, create_calendar_event, send_email, session_type_for

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TODAY = date(2026, 6, 26)  # Friday


def make_meta(
    *,
    last_session_date: str | None = None,
    last_cumulative_review: str | None = "2026-06-20",  # 6 days ago — not overdue
    streak: int = 3,
    phase: int = 0,
    week: int = 1,
    next_up: str = "Watch 3B1B ch. 4",
    total_hours: float = 1.0,
    sessions: int = 2,
) -> dict:
    return {
        "study_streak": streak,
        "current_phase": phase,
        "current_week": week,
        "next_up": next_up,
        "total_hours_logged": total_hours,
        "session_count": sessions,
        "last_session_date": last_session_date,
        "last_cumulative_review": last_cumulative_review,
    }


# ---------------------------------------------------------------------------
# session_type_for
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("offset,expected_type,expected_duration", [
    (0, "weekday-micro", 30),    # Thursday
    (1, "weekday-micro", 30),    # Friday
    (2, "saturday-deep", 180),   # Saturday
    (3, "sunday-deep-review", 120),  # Sunday
    (4, "weekday-micro", 30),    # Monday
    (5, "weekday-micro", 30),    # Tuesday
    (6, "weekday-micro", 30),    # Wednesday
])
def test_session_type_for(offset, expected_type, expected_duration):
    day = date(2026, 6, 25) + timedelta(days=offset)  # 2026-06-25 is a Thursday
    session_type, duration = session_type_for(day)
    assert session_type == expected_type
    assert duration == expected_duration


# ---------------------------------------------------------------------------
# build_email — subject
# ---------------------------------------------------------------------------

def test_subject_contains_phase_week_streak():
    meta = make_meta(streak=5, phase=1, week=2, last_session_date=str(TODAY))
    subject, _, _, _ = build_email(meta, TODAY + timedelta(days=1), today=TODAY)
    assert "Phase 1" in subject
    assert "Week 2" in subject
    assert "streak: 5d" in subject


# ---------------------------------------------------------------------------
# build_email — session type routing
# ---------------------------------------------------------------------------

def test_weekday_session_type():
    tomorrow = date(2026, 6, 29)  # Monday
    meta = make_meta(last_session_date=str(TODAY))
    _, _, session_type, duration = build_email(meta, tomorrow, today=TODAY)
    assert session_type == "weekday-micro"
    assert duration == 30


def test_saturday_session_type():
    tomorrow = date(2026, 6, 27)  # Saturday
    meta = make_meta(last_session_date=str(TODAY))
    _, _, session_type, duration = build_email(meta, tomorrow, today=TODAY)
    assert session_type == "saturday-deep"
    assert duration == 180


def test_sunday_session_type():
    tomorrow = date(2026, 6, 28)  # Sunday
    meta = make_meta(last_session_date=str(TODAY))
    _, _, session_type, duration = build_email(meta, tomorrow, today=TODAY)
    assert session_type == "sunday-deep-review"
    assert duration == 120


# ---------------------------------------------------------------------------
# build_email — biweekly override
# ---------------------------------------------------------------------------

def test_biweekly_overdue_when_null():
    meta = make_meta(last_cumulative_review=None, last_session_date=str(TODAY))
    _, body, session_type, duration = build_email(meta, TODAY + timedelta(days=1), today=TODAY)
    assert session_type == "biweekly-cumulative"
    assert duration == 90
    assert "Biweekly review overdue" in body


def test_biweekly_overdue_when_14_days_ago():
    stale = str(TODAY - timedelta(days=14))
    meta = make_meta(last_cumulative_review=stale, last_session_date=str(TODAY))
    _, body, session_type, _ = build_email(meta, TODAY + timedelta(days=1), today=TODAY)
    assert session_type == "biweekly-cumulative"
    assert "Biweekly review overdue" in body


def test_biweekly_not_overdue_when_recent():
    recent = str(TODAY - timedelta(days=7))
    meta = make_meta(last_cumulative_review=recent, last_session_date=str(TODAY))
    _, body, session_type, _ = build_email(meta, TODAY + timedelta(days=1), today=TODAY)
    assert session_type != "biweekly-cumulative"
    assert "Biweekly review overdue" not in body


# ---------------------------------------------------------------------------
# build_email — streak warning
# ---------------------------------------------------------------------------

def test_streak_warning_when_session_missed():
    yesterday = str(TODAY - timedelta(days=1))
    meta = make_meta(last_session_date=yesterday)
    _, body, _, _ = build_email(meta, TODAY + timedelta(days=1), today=TODAY)
    assert "Streak at risk" in body


def test_no_streak_warning_when_session_today():
    meta = make_meta(last_session_date=str(TODAY))
    _, body, _, _ = build_email(meta, TODAY + timedelta(days=1), today=TODAY)
    assert "Streak at risk" not in body


def test_no_streak_warning_when_no_session_ever():
    meta = make_meta(last_session_date=None)
    _, body, _, _ = build_email(meta, TODAY + timedelta(days=1), today=TODAY)
    assert "Streak at risk" not in body


# ---------------------------------------------------------------------------
# build_email — body always contains next_up
# ---------------------------------------------------------------------------

def test_body_contains_next_up():
    meta = make_meta(next_up="Watch 3B1B chapter 7", last_session_date=str(TODAY))
    _, body, _, _ = build_email(meta, TODAY + timedelta(days=1), today=TODAY)
    assert "Watch 3B1B chapter 7" in body


def test_body_contains_stats():
    meta = make_meta(total_hours=4.5, sessions=9, last_session_date=str(TODAY))
    _, body, _, _ = build_email(meta, TODAY + timedelta(days=1), today=TODAY)
    assert "4.5h" in body
    assert "Sessions: 9" in body


# ---------------------------------------------------------------------------
# send_email — SMTP calls
# ---------------------------------------------------------------------------

def test_send_email_calls_smtp(monkeypatch):
    monkeypatch.setenv("GMAIL_ADDRESS", "test@gmail.com")
    monkeypatch.setenv("GMAIL_APP_PASSWORD", "fake-password")

    mock_smtp = MagicMock()
    mock_smtp.__enter__ = MagicMock(return_value=mock_smtp)
    mock_smtp.__exit__ = MagicMock(return_value=False)

    with patch("smtplib.SMTP", return_value=mock_smtp):
        send_email("Test subject", "Test body")

    mock_smtp.starttls.assert_called_once()
    mock_smtp.login.assert_called_once_with("test@gmail.com", "fake-password")
    mock_smtp.send_message.assert_called_once()


# ---------------------------------------------------------------------------
# create_calendar_event — Google API calls
# ---------------------------------------------------------------------------

def test_create_calendar_event_uses_deterministic_id(monkeypatch):
    fake_token = {
        "token": "tok", "refresh_token": "ref",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "cid", "client_secret": "csec",
        "scopes": ["https://www.googleapis.com/auth/calendar.events"],
    }
    monkeypatch.setenv("GCAL_TOKEN_JSON", json.dumps(fake_token))
    monkeypatch.setenv("GCAL_CALENDAR_ID", "primary")

    mock_service = MagicMock()
    mock_service.events().insert().execute.return_value = {"htmlLink": "https://cal.google.com/event"}

    with patch("remind.Credentials.from_authorized_user_info") as mock_creds, \
         patch("remind.build", return_value=mock_service):
        mock_creds.return_value.expired = False
        create_calendar_event(date(2026, 6, 27), "saturday-deep", "next", 180, 0)

    _, kwargs = mock_service.events().insert.call_args
    assert kwargs["body"]["id"] == "studyreminder20260627"


def test_create_calendar_event_updates_on_duplicate(monkeypatch):
    fake_token = {
        "token": "tok", "refresh_token": "ref",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "cid", "client_secret": "csec",
        "scopes": ["https://www.googleapis.com/auth/calendar.events"],
    }
    monkeypatch.setenv("GCAL_TOKEN_JSON", json.dumps(fake_token))
    monkeypatch.setenv("GCAL_CALENDAR_ID", "primary")

    mock_service = MagicMock()
    conflict = HttpError(resp=MagicMock(status=409), content=b"conflict")
    mock_service.events().insert().execute.side_effect = conflict
    mock_service.events().update().execute.return_value = {"htmlLink": "https://cal.google.com/event"}

    with patch("remind.Credentials.from_authorized_user_info") as mock_creds, \
         patch("remind.build", return_value=mock_service):
        mock_creds.return_value.expired = False
        create_calendar_event(date(2026, 6, 27), "saturday-deep", "next", 180, 0)

    mock_service.events().update.assert_called()


def test_create_calendar_event_builds_correct_event(monkeypatch):
    fake_token = {
        "token": "tok",
        "refresh_token": "ref",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "cid",
        "client_secret": "csec",
        "scopes": ["https://www.googleapis.com/auth/calendar.events"],
    }
    monkeypatch.setenv("GCAL_TOKEN_JSON", json.dumps(fake_token))
    monkeypatch.setenv("GCAL_CALENDAR_ID", "primary")

    mock_service = MagicMock()
    mock_service.events().insert().execute.return_value = {"htmlLink": "https://cal.google.com/event"}

    with patch("remind.Credentials.from_authorized_user_info") as mock_creds, \
         patch("remind.build", return_value=mock_service):

        mock_creds.return_value.expired = False

        create_calendar_event(
            day=date(2026, 6, 27),
            session_type="saturday-deep",
            next_up="Watch 3B1B ch. 4",
            duration_min=180,
            phase=0,
        )

    insert_call = mock_service.events().insert
    _, kwargs = insert_call.call_args
    event = kwargs["body"]

    assert event["summary"] == "Study — saturday-deep · Phase 0"
    assert event["description"] == "Watch 3B1B ch. 4"
    assert event["colorId"] == "7"
    assert "09:00:00" in event["start"]["dateTime"]
    assert "12:00:00" in event["end"]["dateTime"]
    assert event["start"]["timeZone"] == "America/La_Paz"
