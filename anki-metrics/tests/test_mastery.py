from mastery import CardStat, aggregate_topic, classify_card_state


def _stat(interval_days=0, lapses=0, reps=1, card_type=2, note_id=1):
    return CardStat(note_id=note_id, interval_days=interval_days, lapses=lapses, reps=reps, card_type=card_type)


def test_classify_card_state_new():
    assert classify_card_state(_stat(card_type=0)) == "new"


def test_classify_card_state_learning():
    assert classify_card_state(_stat(card_type=1)) == "learning"


def test_classify_card_state_relearning_counts_as_learning():
    assert classify_card_state(_stat(card_type=3)) == "learning"


def test_classify_card_state_young_below_mature_boundary():
    assert classify_card_state(_stat(card_type=2, interval_days=20)) == "young"


def test_classify_card_state_mature_at_exact_boundary():
    assert classify_card_state(_stat(card_type=2, interval_days=21)) == "mature"


def test_aggregate_topic_empty_list_is_no_data():
    stats = aggregate_topic("dot-product", [])
    assert stats.verdict == "no-data"
    assert stats.card_count == 0


def test_aggregate_topic_all_mature_low_lapse_is_solid():
    cards = [_stat(interval_days=30, lapses=0, reps=10, note_id=i) for i in range(5)]
    stats = aggregate_topic("dot-product", cards)
    assert stats.verdict == "solid"
    assert stats.mature_count == 5


def test_aggregate_topic_all_new_is_needs_repass():
    cards = [_stat(card_type=0, note_id=i) for i in range(5)]
    stats = aggregate_topic("dot-product", cards)
    assert stats.verdict == "needs-repass"


def test_aggregate_topic_high_lapse_rate_overrides_mature_ratio():
    # mostly mature, but forgotten a lot -> still needs-repass
    cards = [_stat(interval_days=30, lapses=3, reps=10, note_id=i) for i in range(5)]
    stats = aggregate_topic("dot-product", cards)
    assert stats.lapse_rate == 0.3
    assert stats.verdict == "needs-repass"


def test_aggregate_topic_boundary_is_solid_inclusive():
    # 3/5 mature (0.6), lapse_rate exactly 0.15 -> solid (both boundaries inclusive)
    mature = [_stat(interval_days=30, lapses=0, reps=5, note_id=i) for i in range(3)]
    young = [
        CardStat(note_id=10, interval_days=5, lapses=1, reps=2, card_type=2),
        CardStat(note_id=11, interval_days=5, lapses=2, reps=3, card_type=2),
    ]
    cards = mature + young
    stats = aggregate_topic("dot-product", cards)
    total_reps = sum(c.reps for c in cards)
    total_lapses = sum(c.lapses for c in cards)
    assert stats.mature_count / stats.card_count == 0.6
    assert total_lapses / total_reps == 0.15
    assert stats.verdict == "solid"


def test_aggregate_topic_just_below_solid_boundary_is_developing():
    # mature_ratio 0.59 (not >= 0.6), no lapses, no struggling cards -> developing
    mature = [_stat(interval_days=30, lapses=0, reps=5, note_id=i) for i in range(59)]
    young = [_stat(interval_days=5, lapses=0, reps=5, note_id=i + 100) for i in range(41)]
    cards = mature + young
    stats = aggregate_topic("dot-product", cards)
    assert stats.mature_count / stats.card_count == 0.59
    assert stats.lapse_rate == 0.0
    assert stats.verdict == "developing"


def test_avg_interval_days_excludes_new_and_learning_cards():
    cards = [
        _stat(card_type=0, note_id=1),  # new, interval 0 — excluded
        _stat(card_type=2, interval_days=40, note_id=2),
        _stat(card_type=2, interval_days=20, note_id=3),
    ]
    stats = aggregate_topic("dot-product", cards)
    assert stats.avg_interval_days == 30.0


def test_avg_interval_days_zero_when_all_new():
    cards = [_stat(card_type=0, note_id=i) for i in range(3)]
    stats = aggregate_topic("dot-product", cards)
    assert stats.avg_interval_days == 0.0
