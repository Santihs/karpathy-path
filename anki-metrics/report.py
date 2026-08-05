from datetime import date

from mastery import TopicStats


def render_report(repo: str, run_date: date, topic_stats: dict[str, TopicStats], skipped: int) -> str:
    lines = [f"# Quiz metrics — {repo} — {run_date.isoformat()}", ""]

    needs_repass = [s for s in topic_stats.values() if s.verdict == "needs-repass"]
    solid = [s for s in topic_stats.values() if s.verdict == "solid"]
    developing = [s for s in topic_stats.values() if s.verdict == "developing"]

    if needs_repass:
        lines += ["## ⚠ Needs repass", ""]
        for s in sorted(needs_repass, key=lambda s: s.lapse_rate, reverse=True):
            lines.append(
                f"- **{s.topic}** — {s.card_count} cards, "
                f"{s.lapse_rate:.0%} lapse rate, "
                f"{s.new_count + s.learning_count}/{s.card_count} still new/learning"
            )
        lines.append("")

    lines += ["## ✓ Solid", ""]
    lines.append(", ".join(s.topic for s in sorted(solid, key=lambda s: s.topic)) if solid else "_none yet_")
    lines.append("")

    lines += ["## Developing", ""]
    lines.append(", ".join(s.topic for s in sorted(developing, key=lambda s: s.topic)) if developing else "_none_")
    lines.append("")

    lines += [
        "## Full breakdown",
        "",
        "| Topic | Cards | New | Learning | Young | Mature | Avg interval (d) | Lapse rate | Verdict |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for s in sorted(topic_stats.values(), key=lambda s: s.topic):
        lines.append(
            f"| {s.topic} | {s.card_count} | {s.new_count} | {s.learning_count} | "
            f"{s.young_count} | {s.mature_count} | {s.avg_interval_days:.1f} | "
            f"{s.lapse_rate:.0%} | {s.verdict} |"
        )

    if skipped:
        lines += ["", f"_{skipped} card(s) skipped — noteId not found in Anki (never synced?)._"]

    return "\n".join(lines) + "\n"
