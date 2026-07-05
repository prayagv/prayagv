#!/usr/bin/env python3
"""Generate the quality-signal SVG cards for the profile README.

Fetches recent public GitHub events for USER and renders them as a
test-report-style card in dark and light variants. Runs inside the
quality-signal GitHub Actions workflow on a daily schedule.

Offline usage (renders embedded fixture data, no network):

    python scripts/generate_quality_signal.py --sample --out-dir assets

If the GitHub API call fails the script exits non-zero, the workflow stops
before the commit step, and the previously published cards stay in place.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

USER = "prayagv"
EVENTS_URL = "https://api.github.com/users/{user}/events/public?per_page=100&page={page}"
WINDOW_DAYS = 30
SPARK_DAYS = 14
BAR_MAX_WIDTH = 360
BAR_MIN_WIDTH = 4

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "-apple-system, 'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif"

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "border": "#30363d",
        "text": "#e6edf3",
        "muted": "#8b949e",
        "accent": "#3fb950",
        "accent2": "#58a6ff",
        "bar_bg": "#21262d",
    },
    "light": {
        "bg": "#ffffff",
        "border": "#d0d7de",
        "text": "#1f2328",
        "muted": "#57606a",
        "accent": "#1a7f37",
        "accent2": "#0969da",
        "bar_bg": "#eaeef2",
    },
}


def fetch_events() -> list[dict]:
    """Fetch up to 300 recent public events for USER from the GitHub API."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USER}-profile-quality-signal",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    events: list[dict] = []
    for page in (1, 2, 3):
        url = EVENTS_URL.format(user=USER, page=page)
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.load(response)
        if not batch:
            break
        events.extend(batch)
        if len(batch) < 100:
            break
    return events


def parse_time(stamp: str) -> datetime:
    return datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def summarize(events: list[dict], now: datetime) -> dict:
    """Reduce raw GitHub events to the counters the card displays."""
    window_start = now - timedelta(days=WINDOW_DAYS)
    commits = prs_opened = prs_merged = reviews = 0
    repos: set[str] = set()
    per_day = [0] * SPARK_DAYS

    for event in events:
        created = parse_time(event["created_at"])
        if created < window_start:
            continue

        age_days = (now - created).days
        if 0 <= age_days < SPARK_DAYS:
            per_day[SPARK_DAYS - 1 - age_days] += 1

        payload = event.get("payload") or {}
        repo = (event.get("repo") or {}).get("name")
        event_type = event.get("type")

        if event_type == "PushEvent":
            commits += int(payload.get("size") or 0)
            if repo:
                repos.add(repo)
        elif event_type == "PullRequestEvent":
            action = payload.get("action")
            pull_request = payload.get("pull_request") or {}
            if action == "opened":
                prs_opened += 1
            if action == "closed" and pull_request.get("merged"):
                prs_merged += 1
            if repo:
                repos.add(repo)
        elif event_type == "PullRequestReviewEvent":
            reviews += 1
            if repo:
                repos.add(repo)

    return {
        "commits": commits,
        "prs_opened": prs_opened,
        "prs_merged": prs_merged,
        "reviews": reviews,
        "repos": len(repos),
        "per_day": per_day,
        "generated": now.strftime("%Y-%m-%d"),
    }


def bar_width(value: int, max_value: int) -> int:
    if value <= 0 or max_value <= 0:
        return 0
    return max(BAR_MIN_WIDTH, round(BAR_MAX_WIDTH * value / max_value))


def _status_icon(cx: int, cy: int, ok: bool, theme: dict) -> str:
    if ok:
        return (
            f'<circle cx="{cx}" cy="{cy}" r="8" fill="none" stroke="{theme["accent"]}" stroke-width="1.6"/>'
            f'<path d="M{cx - 3.8} {cy + 0.4} l2.6 2.6 l5.0 -5.6" fill="none" stroke="{theme["accent"]}"'
            f' stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    return (
        f'<circle cx="{cx}" cy="{cy}" r="8" fill="none" stroke="{theme["muted"]}" stroke-width="1.6"/>'
        f'<line x1="{cx - 4}" y1="{cy}" x2="{cx + 4}" y2="{cy}" stroke="{theme["muted"]}"'
        f' stroke-width="1.8" stroke-linecap="round"/>'
    )


def render(summary: dict, theme_name: str) -> str:
    theme = THEMES[theme_name]
    rows = [
        ("commits pushed", summary["commits"],
         f"across {summary['repos']} public repo{'s' if summary['repos'] != 1 else ''}"),
        ("pull requests opened", summary["prs_opened"], f"{summary['prs_merged']} merged"),
        ("code reviews", summary["reviews"], "PR reviews submitted"),
        ("repos touched", summary["repos"], "distinct public repositories"),
    ]
    max_value = max(value for _, value, _ in rows)
    all_quiet = max_value == 0

    parts = [
        f'<svg width="880" height="300" viewBox="0 0 880 300" xmlns="http://www.w3.org/2000/svg" role="img"'
        f' aria-label="Summary of recent public GitHub activity for {USER}, rendered as a test report">',
        f'<rect x="0.5" y="0.5" width="879" height="299" rx="11.5" fill="{theme["bg"]}" stroke="{theme["border"]}"/>',
        f'<circle cx="32" cy="32" r="5" fill="{theme["accent"]}">'
        f'<animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/></circle>',
        f'<text x="46" y="37" font-family="{MONO}" font-size="14" font-weight="700" fill="{theme["text"]}">quality-signal</text>',
        f'<text x="848" y="37" text-anchor="end" font-family="{MONO}" font-size="12" fill="{theme["muted"]}">'
        f'updated {summary["generated"]} · public events · last {WINDOW_DAYS} days</text>',
        f'<line x1="32" y1="54" x2="848" y2="54" stroke="{theme["border"]}"/>',
    ]

    if all_quiet:
        parts.append(
            f'<text x="32" y="76" font-family="{SANS}" font-size="12" font-style="italic" fill="{theme["muted"]}">'
            "quiet on public GitHub right now — the pinned repos hold the long-form evidence</text>"
        )

    y = 92
    for label, value, note in rows:
        parts.append(_status_icon(44, y - 5, value > 0, theme))
        parts.append(
            f'<text x="66" y="{y}" font-family="{MONO}" font-size="13" fill="{theme["text"]}">{label}</text>'
        )
        parts.append(
            f'<text x="286" y="{y}" text-anchor="end" font-family="{MONO}" font-size="13" font-weight="700"'
            f' fill="{theme["text"]}">{value}</text>'
        )
        parts.append(
            f'<rect x="300" y="{y - 13}" width="{BAR_MAX_WIDTH}" height="10" rx="5" fill="{theme["bar_bg"]}"/>'
        )
        width = bar_width(value, max_value)
        if width > 0:
            parts.append(
                f'<rect x="300" y="{y - 13}" width="{width}" height="10" rx="5" fill="{theme["accent"]}"/>'
            )
        parts.append(
            f'<text x="674" y="{y}" font-family="{SANS}" font-size="12" fill="{theme["muted"]}">{note}</text>'
        )
        y += 36

    parts.append(
        f'<text x="32" y="246" font-family="{MONO}" font-size="11" fill="{theme["muted"]}">'
        f"events per day · last {SPARK_DAYS} days</text>"
    )
    spark_max = max(summary["per_day"]) if summary["per_day"] else 0
    x = 32
    for count in summary["per_day"]:
        if spark_max > 0 and count > 0:
            height = 2 + round(32 * count / spark_max)
            color = theme["accent2"]
        else:
            height = 2
            color = theme["bar_bg"]
        parts.append(
            f'<rect x="{x}" y="{284 - height}" width="16" height="{height}" rx="1.5" fill="{color}"/>'
        )
        x += 24

    parts.append(
        f'<text x="848" y="284" text-anchor="end" font-family="{MONO}" font-size="11" fill="{theme["muted"]}">'
        "generated by a scheduled GitHub Action · unit-tested before every publish</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def sample_events(now: datetime) -> list[dict]:
    """Deterministic fixture data so the card can be rendered offline."""
    repos = [
        "qa-test-automation-frameworks/aria-api-framework",
        "qa-test-automation-frameworks/k6-performance-framework",
        "qa-test-automation-frameworks/playwright-typescript-framework",
        "qa-test-automation-frameworks/verity-policy-coverage-eval-framework",
    ]
    events = []
    for day in range(SPARK_DAYS):
        stamp = (now - timedelta(days=day, hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
        repo = repos[day % len(repos)]
        if day % 2 == 0:
            events.append({"type": "PushEvent", "created_at": stamp,
                           "payload": {"size": (day % 3) + 1}, "repo": {"name": repo}})
        if day % 5 == 1:
            events.append({"type": "PullRequestEvent", "created_at": stamp,
                           "payload": {"action": "opened"}, "repo": {"name": repo}})
        if day % 5 == 3:
            events.append({"type": "PullRequestEvent", "created_at": stamp,
                           "payload": {"action": "closed", "pull_request": {"merged": True}},
                           "repo": {"name": repo}})
        if day % 4 == 2:
            events.append({"type": "PullRequestReviewEvent", "created_at": stamp,
                           "payload": {}, "repo": {"name": repo}})
    return events


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", action="store_true",
                        help="render embedded fixture data instead of calling the GitHub API")
    parser.add_argument("--out-dir", default="assets", help="directory for the generated SVGs")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    try:
        events = sample_events(now) if args.sample else fetch_events()
    except Exception as error:  # noqa: BLE001 — any fetch failure must block publishing
        print(f"quality-signal: failed to fetch events, keeping previous cards: {error}",
              file=sys.stderr)
        return 1

    summary = summarize(events, now)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for theme_name in THEMES:
        target = out_dir / f"quality-signal-{theme_name}.svg"
        target.write_text(render(summary, theme_name), encoding="utf-8")
        print(f"quality-signal: wrote {target}")
    print(f"quality-signal: {summary['commits']} commits, {summary['prs_opened']} PRs opened, "
          f"{summary['reviews']} reviews across {summary['repos']} repos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
