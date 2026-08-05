from datetime import date

from mastery import TopicStats
from report import render_report


def _stats(topic, verdict, **overrides):
    defaults = dict(
        topic=topic,
        card_count=4,
        new_count=0,
        learning_count=0,
        young_count=1,
        mature_count=3,
        avg_interval_days=25.0,
        lapse_rate=0.1,
        verdict=verdict,
    )
    defaults.update(overrides)
    return TopicStats(**defaults)


def test_needs_repass_section_omitted_when_none():
    stats = {"dot-product": _stats("dot-product", "solid")}
    report = render_report("karpathy", date(2026, 8, 4), stats, skipped=0)
    assert "Needs repass" not in report


def test_needs_repass_section_present_and_sorted_by_lapse_rate():
    stats = {
        "topic-a": _stats("topic-a", "needs-repass", lapse_rate=0.3),
        "topic-b": _stats("topic-b", "needs-repass", lapse_rate=0.6),
    }
    report = render_report("karpathy", date(2026, 8, 4), stats, skipped=0)
    a_idx = report.index("topic-a")
    b_idx = report.index("topic-b")
    assert b_idx < a_idx  # higher lapse rate (topic-b) listed first


def test_topics_bucketed_into_correct_sections():
    stats = {
        "solid-topic": _stats("solid-topic", "solid"),
        "dev-topic": _stats("dev-topic", "developing"),
        "bad-topic": _stats("bad-topic", "needs-repass"),
    }
    report = render_report("karpathy", date(2026, 8, 4), stats, skipped=0)
    solid_section = report.split("## Developing")[0].split("## ✓ Solid")[1]
    assert "solid-topic" in solid_section
    assert "dev-topic" not in solid_section


def test_skipped_footnote_only_when_nonzero():
    stats = {"dot-product": _stats("dot-product", "solid")}
    with_skipped = render_report("karpathy", date(2026, 8, 4), stats, skipped=2)
    without_skipped = render_report("karpathy", date(2026, 8, 4), stats, skipped=0)
    assert "skipped" in with_skipped
    assert "skipped" not in without_skipped


def test_full_breakdown_table_row_formatting():
    stats = {"dot-product": _stats("dot-product", "solid", card_count=5, new_count=0, learning_count=0,
                                    young_count=1, mature_count=4, avg_interval_days=22.5, lapse_rate=0.1)}
    report = render_report("karpathy", date(2026, 8, 4), stats, skipped=0)
    assert "| dot-product | 5 | 0 | 0 | 1 | 4 | 22.5 | 10% | solid |" in report
