from pathlib import Path

from metrics import build_topic_stats
from quizbank import Card


def _raw_card(interval=30, lapses=0, reps=10, card_type=2):
    return {"interval": interval, "lapses": lapses, "reps": reps, "type": card_type}


def test_build_topic_stats_aggregates_multi_topic_card_into_each_topic():
    cards = [Card(path=Path("a.md"), note_id=1, tags=["repo-karpathy", "dot-product", "duality"])]
    note_cards = {1: _raw_card()}

    topic_stats, skipped = build_topic_stats(cards, note_cards)

    assert skipped == 0
    assert set(topic_stats.keys()) == {"dot-product", "duality"}
    assert topic_stats["dot-product"].card_count == 1


def test_build_topic_stats_counts_cards_missing_from_anki_as_skipped():
    cards = [
        Card(path=Path("a.md"), note_id=1, tags=["repo-karpathy", "dot-product"]),
        Card(path=Path("b.md"), note_id=2, tags=["repo-karpathy", "dot-product"]),
    ]
    note_cards = {1: _raw_card()}  # note_id 2 never synced / not found in Anki

    topic_stats, skipped = build_topic_stats(cards, note_cards)

    assert skipped == 1
    assert topic_stats["dot-product"].card_count == 1
