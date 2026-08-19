"""Generate compatibility redirects for old or mistakenly shared post URLs."""

from __future__ import annotations

import html
import json
from datetime import date, datetime
from pathlib import Path, PurePosixPath

import yaml


def _as_date(value: object) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _load_metadata(path: Path) -> dict[str, object]:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path}: missing YAML front matter")
    return yaml.safe_load(parts[1]) or {}


def _safe_alias(alias: object) -> str:
    value = str(alias).strip().lstrip("/")
    path = PurePosixPath(value)
    if (
        not value.endswith("/")
        or path.is_absolute()
        or ".." in path.parts
        or not value.startswith("blog/")
    ):
        raise ValueError(f"Unsafe post redirect path: {alias!r}")
    return value


def _redirect_html(canonical_url: str) -> str:
    escaped_url = html.escape(canonical_url, quote=True)
    js_url = json.dumps(canonical_url)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={escaped_url}">
    <link rel="canonical" href="{escaped_url}">
    <meta name="robots" content="noindex">
    <title>Redirecting…</title>
    <script>
      window.location.replace(
        {js_url} + window.location.search + window.location.hash
      );
    </script>
  </head>
  <body>
    <p>This post has moved to <a href="{escaped_url}">{escaped_url}</a>.</p>
  </body>
</html>
"""


def on_post_build(config):
    """Write redirect pages after MkDocs and the blog plugin finish building."""
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])
    site_url = str(config["site_url"]).rstrip("/")

    for post_path in sorted((docs_dir / "blog" / "posts").glob("*.md")):
        metadata = _load_metadata(post_path)
        aliases = metadata.get("redirect_from") or []
        if not aliases:
            continue

        post_date = _as_date(metadata["date"])
        slug = str(metadata["slug"])
        canonical_url = (
            f"{site_url}/blog/{post_date:%Y/%m/%d}/{slug}/"
        )

        for raw_alias in aliases:
            alias = _safe_alias(raw_alias)
            output = site_dir / alias / "index.html"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                _redirect_html(canonical_url),
                encoding="utf-8",
            )
