"""Generate date-aware series links on the quantum landing page."""

from __future__ import annotations

import os
import re
from datetime import date, datetime, timezone
from pathlib import Path

import yaml


START = "<!-- bottleneck-posts:start -->"
END = "<!-- bottleneck-posts:end -->"
SERIES = "The Quantum Bottleneck"
POST_PATTERN = "blog/posts/bottleneck-*.md"


def _as_date(value: object) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _today() -> date:
    override = os.environ.get("QUANTUM_LANDING_AS_OF")
    return date.fromisoformat(override) if override else datetime.now(timezone.utc).date()


def _load_posts(docs_dir: Path) -> list[dict[str, object]]:
    posts: list[dict[str, object]] = []
    for path in sorted(docs_dir.glob(POST_PATTERN)):
        content = path.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError(f"{path}: missing YAML front matter")

        metadata = yaml.safe_load(parts[1]) or {}
        categories = metadata.get("categories") or []
        if SERIES not in categories:
            continue

        title_match = re.search(r"^#\s+(.+)$", parts[2], re.MULTILINE)
        if not title_match:
            raise ValueError(f"{path}: missing H1 title")

        for field in ("date", "slug", "landing_summary"):
            if not metadata.get(field):
                raise ValueError(f"{path}: missing required landing-page field '{field}'")

        posts.append(
            {
                "date": _as_date(metadata["date"]),
                "slug": str(metadata["slug"]),
                "summary": " ".join(str(metadata["landing_summary"]).split()),
                "title": title_match.group(1).strip(),
            }
        )

    return sorted(posts, key=lambda post: post["date"])


def _render(posts: list[dict[str, object]], as_of: date) -> str:
    published = [post for post in posts if post["date"] <= as_of]
    upcoming = [post for post in posts if post["date"] > as_of]

    lines: list[str] = [START]
    for post in published:
        post_date = post["date"]
        url = (
            f"blog/{post_date:%Y/%m/%d}/{post['slug']}/"
        )
        lines.append(f"- [{post['title']}]({url}) — {post['summary']}")

    lines.extend(
        [
            "- [Series overview and companion notebooks](bottleneck/) — "
            "the full eight-part path and its runnable notebooks.",
            "- [Circuit Bench](circuit-bench/) — thirteen circuit notes with "
            "diagrams, OpenQASM, expected output, and gate-by-gate explanations.",
        ]
    )

    if upcoming:
        next_post = upcoming[0]
        next_date = next_post["date"]
        lines.extend(
            [
                "",
                f"Next up: **{next_post['title']}** on "
                f"{next_date.day} {next_date.strftime('%B')} — "
                f"{next_post['summary']}",
            ]
        )
    elif posts:
        lines.extend(["", "The complete eight-part series is now live."])

    lines.append(END)
    return "\n".join(lines)


def on_page_markdown(markdown, page, config, files):
    """Replace the marked landing-page block during every MkDocs build."""
    if page.file.src_uri != "index.md":
        return markdown

    if START not in markdown or END not in markdown:
        raise ValueError("docs/index.md is missing the Bottleneck generation markers")

    replacement = _render(_load_posts(Path(config["docs_dir"])), _today())
    pattern = re.compile(f"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    return pattern.sub(lambda _match: replacement, markdown, count=1)
