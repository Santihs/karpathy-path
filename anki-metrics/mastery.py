from dataclasses import dataclass

# Anki's own young/mature boundary — reused rather than inventing a new one.
MATURE_INTERVAL_DAYS = 21

# More than 1-in-4 reviews on a topic were "Again" -> needs repass regardless of interval length.
NEEDS_REPASS_LAPSE_RATE = 0.25
# Half or more of a topic's cards still new/learning -> not enough signal yet, needs attention.
NEEDS_REPASS_STRUGGLING_RATIO = 0.5
# "solid" requires both a majority mature AND a low lapse rate — long intervals with a high
# forget-rate isn't actually solid, just under-tested.
SOLID_MATURE_RATIO = 0.6
SOLID_LAPSE_RATE = 0.15


@dataclass(frozen=True)
class CardStat:
    note_id: int
    interval_days: int
    lapses: int
    reps: int
    card_type: int  # 0=new, 1=learning, 2=review, 3=relearning


@dataclass(frozen=True)
class TopicStats:
    topic: str
    card_count: int
    new_count: int
    learning_count: int
    young_count: int
    mature_count: int
    avg_interval_days: float
    lapse_rate: float
    verdict: str  # "solid" | "developing" | "needs-repass" | "no-data"


def classify_card_state(card: CardStat) -> str:
    if card.card_type == 0:
        return "new"
    if card.card_type in (1, 3):
        return "learning"
    return "mature" if card.interval_days >= MATURE_INTERVAL_DAYS else "young"


def classify_topic(
    card_count: int,
    mature_count: int,
    young_count: int,
    new_count: int,
    learning_count: int,
    lapse_rate: float,
) -> str:
    if card_count == 0:
        return "no-data"

    mature_ratio = mature_count / card_count
    struggling_ratio = (new_count + learning_count) / card_count

    if lapse_rate > NEEDS_REPASS_LAPSE_RATE or struggling_ratio >= NEEDS_REPASS_STRUGGLING_RATIO:
        return "needs-repass"
    if mature_ratio >= SOLID_MATURE_RATIO and lapse_rate <= SOLID_LAPSE_RATE:
        return "solid"
    return "developing"


def aggregate_topic(topic: str, cards: list[CardStat]) -> TopicStats:
    if not cards:
        return TopicStats(topic, 0, 0, 0, 0, 0, 0.0, 0.0, "no-data")

    states = [classify_card_state(c) for c in cards]
    new_count = states.count("new")
    learning_count = states.count("learning")
    young_count = states.count("young")
    mature_count = states.count("mature")

    reviewed = [c for c, s in zip(cards, states) if s in ("young", "mature")]
    avg_interval = sum(c.interval_days for c in reviewed) / len(reviewed) if reviewed else 0.0

    total_reps = sum(c.reps for c in cards)
    total_lapses = sum(c.lapses for c in cards)
    lapse_rate = total_lapses / total_reps if total_reps else 0.0

    verdict = classify_topic(len(cards), mature_count, young_count, new_count, learning_count, lapse_rate)

    return TopicStats(
        topic=topic,
        card_count=len(cards),
        new_count=new_count,
        learning_count=learning_count,
        young_count=young_count,
        mature_count=mature_count,
        avg_interval_days=avg_interval,
        lapse_rate=lapse_rate,
        verdict=verdict,
    )
