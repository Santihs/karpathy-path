import argparse
from datetime import date
from pathlib import Path

from ankiconnect import ANKICONNECT_URL, AnkiConnectError, cards_info_by_note_id
from mastery import CardStat, aggregate_topic
from quizbank import load_quiz_bank, topics_for
from report import render_report


def build_topic_stats(cards, note_cards):
    by_topic: dict[str, list[CardStat]] = {}
    skipped = 0
    for card in cards:
        raw = note_cards.get(card.note_id)
        if raw is None:
            skipped += 1
            continue
        stat = CardStat(
            note_id=card.note_id,
            interval_days=max(raw["interval"], 0),
            lapses=raw["lapses"],
            reps=raw["reps"],
            card_type=raw["type"],
        )
        for topic in topics_for(card.tags):
            by_topic.setdefault(topic, []).append(stat)
    return {t: aggregate_topic(t, cs) for t, cs in sorted(by_topic.items())}, skipped


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, help="Quiz-bank dir, e.g. 04-Quiz-Bank/devtalles")
    parser.add_argument("--repo", required=True, choices=["karpathy", "devtalles"])
    parser.add_argument("--out", required=True, help="Report file path to write")
    parser.add_argument("--ankiconnect-url", default=ANKICONNECT_URL)
    args = parser.parse_args()

    cards = load_quiz_bank(Path(args.dir))
    if not cards:
        raise SystemExit(f"No cards with noteId found in {args.dir}")

    note_ids = [c.note_id for c in cards]
    try:
        note_cards = cards_info_by_note_id(note_ids, url=args.ankiconnect_url)
    except AnkiConnectError as e:
        raise SystemExit(f"AnkiConnect error: {e}\nIs Anki Desktop open with AnkiConnect installed?")

    topic_stats, skipped = build_topic_stats(cards, note_cards)
    report_md = render_report(args.repo, date.today(), topic_stats, skipped)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_md, encoding="utf-8")
    print(f"Wrote report: {out_path}")

    needs_repass = [t for t, s in topic_stats.items() if s.verdict == "needs-repass"]
    if needs_repass:
        print(f"Needs repass: {', '.join(needs_repass)}")


if __name__ == "__main__":
    main()
