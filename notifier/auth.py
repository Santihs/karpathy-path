"""
One-time local OAuth2 setup for Google Calendar.

Run this once:
    uv run notifier/auth.py

It will open a browser, ask you to log in to Google, then print the
token JSON. Copy that JSON into the GCAL_TOKEN_JSON GitHub Secret.
"""

import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
TOKEN_FILE = Path(__file__).parent / "token.json"


def main() -> None:
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            "notifier/credentials.json not found.\n"
            "Download it from Google Cloud Console:\n"
            "  APIs & Services → Credentials → OAuth 2.0 Client (Desktop) → Download JSON\n"
            "Save it as notifier/credentials.json (it is gitignored)."
        )

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
    creds = flow.run_local_server(port=0)

    token_data = json.loads(creds.to_json())
    token_str = json.dumps(token_data, indent=2)

    TOKEN_FILE.write_text(token_str)

    print("\n" + "=" * 60)
    print("Copy everything below into the GCAL_TOKEN_JSON GitHub Secret:")
    print("=" * 60)
    print(token_str)
    print("=" * 60)
    print(f"\nAlso saved to {TOKEN_FILE} (gitignored).")


if __name__ == "__main__":
    main()
