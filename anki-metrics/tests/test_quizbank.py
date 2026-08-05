from pathlib import Path

import quizbank

VALID_CARD = """---
tags:
  - repo-karpathy
  - phase-0
  - dot-product
  - duality
noteId: 1785651973545
---
What is a vector?

---

An element of a vector space.
"""

NO_FRONTMATTER = "just some text, no frontmatter\n"

NO_NOTE_ID = """---
tags:
  - repo-karpathy
---
front

---

back
"""


def test_parse_card_valid():
    card = quizbank.parse_card(VALID_CARD, Path("foo.md"))
    assert card.note_id == 1785651973545
    assert card.tags == ["repo-karpathy", "phase-0", "dot-product", "duality"]


def test_parse_card_no_frontmatter_returns_none():
    assert quizbank.parse_card(NO_FRONTMATTER, Path("foo.md")) is None


def test_parse_card_missing_note_id_returns_none():
    assert quizbank.parse_card(NO_NOTE_ID, Path("foo.md")) is None


def test_topics_for_strips_repo_and_phase_tags():
    tags = ["repo-karpathy", "phase-0", "dot-product", "duality"]
    assert quizbank.topics_for(tags) == ["dot-product", "duality"]


def test_topics_for_keeps_multi_topic_cards_intact():
    tags = ["repo-devtalles", "workflow-commands", "ollama"]
    assert quizbank.topics_for(tags) == ["workflow-commands", "ollama"]


def test_load_quiz_bank_skips_cards_without_note_id(tmp_path):
    (tmp_path / "valid.md").write_text(VALID_CARD, encoding="utf-8")
    (tmp_path / "no-note-id.md").write_text(NO_NOTE_ID, encoding="utf-8")
    (tmp_path / "not-markdown.txt").write_text("ignored", encoding="utf-8")

    cards = quizbank.load_quiz_bank(tmp_path)

    assert len(cards) == 1
    assert cards[0].note_id == 1785651973545
