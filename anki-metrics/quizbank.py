import re
from dataclasses import dataclass
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"^---\n([\s\S]*?)\n---\n", re.MULTILINE)
SKIPPED_TAG_PREFIXES = ("repo-", "phase-")


@dataclass(frozen=True)
class Card:
    path: Path
    note_id: int
    tags: list[str]


def parse_card(raw: str, path: Path) -> Card | None:
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return None
    frontmatter = yaml.safe_load(match.group(1)) or {}
    note_id = frontmatter.get("noteId")
    tags = frontmatter.get("tags") or []
    if note_id is None:
        return None
    return Card(path=path, note_id=int(note_id), tags=[str(t) for t in tags])


def topics_for(tags: list[str]) -> list[str]:
    return [t for t in tags if not t.startswith(SKIPPED_TAG_PREFIXES)]


def load_quiz_bank(dir_path: Path) -> list[Card]:
    cards = []
    for md_file in sorted(dir_path.glob("*.md")):
        raw = md_file.read_text(encoding="utf-8")
        card = parse_card(raw, md_file)
        if card is not None:
            cards.append(card)
    return cards
