"""Unit tests for the quality-signal card generator.

The quality-signal workflow runs these before regenerating the SVGs; a red
test blocks publishing, so the profile never ships a card the suite has not
covered.
"""

import unittest
from datetime import datetime, timedelta, timezone

import generate_quality_signal as gqs

NOW = datetime(2026, 7, 4, 12, 0, tzinfo=timezone.utc)
REPO = "qa-test-automation-frameworks/aria-api-framework"


def event(event_type, days_ago, payload=None, repo=REPO):
    stamp = (NOW - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"type": event_type, "created_at": stamp,
            "payload": payload or {}, "repo": {"name": repo}}


class SummarizeTests(unittest.TestCase):
    def test_counts_commits_prs_reviews_and_repos(self):
        events = [
            event("PushEvent", 1, {"size": 3}),
            event("PushEvent", 2, {"size": 2}, repo="org/other-repo"),
            event("PullRequestEvent", 3, {"action": "opened"}),
            event("PullRequestEvent", 3, {"action": "closed", "pull_request": {"merged": True}}),
            event("PullRequestReviewEvent", 4),
        ]
        summary = gqs.summarize(events, NOW)
        self.assertEqual(summary["commits"], 5)
        self.assertEqual(summary["prs_opened"], 1)
        self.assertEqual(summary["prs_merged"], 1)
        self.assertEqual(summary["reviews"], 1)
        self.assertEqual(summary["repos"], 2)

    def test_events_outside_window_are_ignored(self):
        events = [event("PushEvent", gqs.WINDOW_DAYS + 15, {"size": 9})]
        summary = gqs.summarize(events, NOW)
        self.assertEqual(summary["commits"], 0)
        self.assertEqual(summary["repos"], 0)

    def test_empty_events_produce_zeroed_summary(self):
        summary = gqs.summarize([], NOW)
        self.assertEqual(summary["commits"], 0)
        self.assertEqual(summary["prs_opened"], 0)
        self.assertEqual(summary["reviews"], 0)
        self.assertEqual(len(summary["per_day"]), gqs.SPARK_DAYS)
        self.assertEqual(sum(summary["per_day"]), 0)

    def test_per_day_places_today_in_last_bucket(self):
        summary = gqs.summarize([event("PushEvent", 0, {"size": 1})], NOW)
        self.assertEqual(summary["per_day"][-1], 1)

    def test_unmerged_close_is_not_counted_as_merge(self):
        events = [event("PullRequestEvent", 1,
                        {"action": "closed", "pull_request": {"merged": False}})]
        summary = gqs.summarize(events, NOW)
        self.assertEqual(summary["prs_merged"], 0)


class BarWidthTests(unittest.TestCase):
    def test_zero_value_has_no_bar(self):
        self.assertEqual(gqs.bar_width(0, 10), 0)

    def test_max_value_fills_the_track(self):
        self.assertEqual(gqs.bar_width(10, 10), gqs.BAR_MAX_WIDTH)

    def test_small_values_stay_visible(self):
        self.assertGreaterEqual(gqs.bar_width(1, 1000), gqs.BAR_MIN_WIDTH)

    def test_width_is_proportional(self):
        self.assertEqual(gqs.bar_width(5, 10), round(gqs.BAR_MAX_WIDTH / 2))


class RenderTests(unittest.TestCase):
    def test_render_produces_valid_card_for_both_themes(self):
        summary = gqs.summarize(gqs.sample_events(NOW), NOW)
        for theme_name, theme in gqs.THEMES.items():
            svg = gqs.render(summary, theme_name)
            self.assertIn("<svg", svg)
            self.assertIn("</svg>", svg)
            self.assertIn("commits pushed", svg)
            self.assertIn(theme["bg"], svg)
            self.assertIn(f"updated {summary['generated']}", svg)

    def test_zero_activity_renders_fallback_note(self):
        summary = gqs.summarize([], NOW)
        svg = gqs.render(summary, "dark")
        self.assertIn("quiet on public GitHub", svg)


if __name__ == "__main__":
    unittest.main()
