"""All publication calls are mocked; these tests cannot consume a posting slot."""

from datetime import datetime, timedelta
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
import urllib.error

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import social_publish as s

NOW = datetime(2026, 9, 15, 12, tzinfo=s.UTC)
OLD = (NOW - timedelta(days=3)).isoformat()
FUTURE = (NOW + timedelta(days=1)).isoformat()


def body(copy="A reproducible demo is ready"):
    values = [
        copy,
        "A working reproducibility milestone",
        "https://github.com/entrotter/entrotter/pull/1",
        "_No response_",
        "_No response_",
    ]
    return "\n\n".join(
        "### " + name + "\n\n" + value for name, value in zip(s.FIELDS, values)
    )


def issue(number=1, labels=None, at=OLD):
    return {
        "number": number,
        "state": "open",
        "body": body(),
        "updated_at": at,
        "labels": [
            {"name": n}
            for n in (
                labels
                if labels is not None
                else ["social:candidate", "social:approved"]
            )
        ],
    }


def draft(number=1, state="published", date=OLD, posts=1):
    return {
        "id": number,
        "social_set_id": 123,
        "status": state,
        "publish_state": None,
        "created_at": OLD,
        "updated_at": OLD,
        "published_at": date if state == "published" else None,
        "scheduled_date": date,
        "draft_title": None,
        "platforms": {
            "x": {
                "enabled": True,
                "posts": [{"text": "A reproducible demo is ready"}] * posts,
            }
        },
    }


def candidate(number=1):
    return {
        "issue": number,
        "copy": "A reproducible demo is ready",
        "body": body(),
        "updated_at": OLD,
        "approved_at": s.timestamp(OLD),
        "priority": 3,
    }


def reservation(number=1):
    return {
        "kind": "reserved",
        "issue": number,
        "at": NOW.isoformat(),
        "copy_sha256": s.digest(candidate()["copy"]),
    }


def accepted(number=1, draft_id=1234):
    return {
        **reservation(number),
        "kind": "accepted",
        "draft_id": draft_id,
        "scheduled_date": FUTURE,
        "result": "scheduled",
    }


def comment(record):
    return {
        "body": s.MARKER + json.dumps(record),
        "user": {"login": "github-actions[bot]"},
    }


class MemoryGH:
    def __init__(self):
        self.comments = []
        self.items = [candidate()]
        self.finished = []
        self.events = []
        self.fail_append = False
        self.fail_finish = False

    def journal(self):
        return s.parse_journal(self.comments)

    def candidates(self, records):
        return [
            c for c in self.items if c["issue"] not in {r["issue"] for r in records}
        ]

    def append(self, record):
        self.events.append(record["kind"])
        if self.fail_append:
            raise s.Skip("SKIP: journal write failed")
        self.comments.append(comment(record))

    def finish(self, number, record):
        self.events.append("finish")
        if self.fail_finish:
            raise s.Skip("SKIP: labels failed")
        self.finished.append(number)


class Guards(unittest.TestCase):
    def test_counts_zero_through_nine_allow(self):
        for count in range(10):
            with self.subTest(count=count):
                s.guard([draft(n + 1) for n in range(count)], [], candidate(), NOW)

    def test_ten_and_above_block(self):
        for count in (10, 11, 50):
            with self.subTest(count=count), self.assertRaisesRegex(s.Skip, "monthly"):
                s.guard([draft(n + 1) for n in range(count)], [], candidate(), NOW)

    def test_thread_and_multiplatform_are_counted_conservatively(self):
        d = draft(posts=5)
        d["platforms"]["linkedin"] = {"enabled": True, "posts": [{"text": "test"}] * 5}
        with self.assertRaisesRegex(s.Skip, "monthly"):
            s.guard([d], [], candidate(), NOW)

    def test_48_hour_boundary(self):
        for hours, blocked in ((47.999, True), (48, False), (49, False)):
            d = draft(date=(NOW - timedelta(hours=hours)).isoformat())
            if blocked:
                with self.assertRaisesRegex(s.Skip, "48-hour"):
                    s.guard([d], [], candidate(), NOW)
            else:
                s.guard([d], [], candidate(), NOW)

    def test_recent_scheduling_and_future_timestamp_block(self):
        for field in ("created_at", "updated_at"):
            for time in (NOW - timedelta(hours=1), NOW + timedelta(hours=1)):
                d = draft(state="scheduled", date=FUTURE)
                d[field] = time.isoformat()
                with (
                    self.subTest(field=field),
                    self.assertRaisesRegex(s.Skip, "48-hour"),
                ):
                    s.guard([d], [], candidate(), NOW)

    def test_future_month_full_blocks_next_free_slot(self):
        with self.assertRaisesRegex(s.Skip, "monthly"):
            s.guard(
                [draft(n + 1, "scheduled", "2026-10-01T12:00:00Z") for n in range(10)],
                [],
                candidate(),
                NOW,
            )

    def test_previous_month_quota_expires(self):
        ds = [draft(n + 1, date="2026-08-15T00:00:00Z") for n in range(10)]
        for d in ds:
            d["created_at"] = d["updated_at"] = d["published_at"]
        s.guard(ds, [], candidate(), NOW)

    def test_boundary_window(self):
        with self.assertRaisesRegex(s.Skip, "month-boundary"):
            s.guard([], [], candidate(), datetime(2026, 9, 30, 23, 55, tzinfo=s.UTC))

    def test_ambiguous_states_block(self):
        for state in ("error", "publishing", "unknown"):
            with self.subTest(state=state), self.assertRaises(s.Skip):
                s.guard([draft(state=state)], [], candidate(), NOW)
        d = draft(state="draft")
        d["publish_state"] = "in_progress"
        with self.assertRaises(s.Skip):
            s.guard([d], [], candidate(), NOW)

    def test_overdue_scheduled_and_missing_date_block(self):
        for date in (OLD, None, "garbage", "2026-09-20T00:00:00"):
            with self.subTest(date=date), self.assertRaises(s.Skip):
                s.guard([draft(state="scheduled", date=date)], [], candidate(), NOW)

    def test_duplicate_candidate_title_or_journal_blocks(self):
        d = draft()
        d["draft_title"] = "entrotter/entrotter#1"
        with self.assertRaises(s.Skip):
            s.guard([d], [], candidate(), NOW)
        with self.assertRaises(s.Skip):
            s.guard([], [reservation(), accepted()], candidate(), NOW)

    def test_ledger_retains_deleted_drafts_and_deduplicates_observed(self):
        records = []
        for n in range(1, 11):
            r, a = reservation(n), accepted(n, n)
            r["at"] = a["at"] = OLD
            a["scheduled_date"] = OLD
            records += [r, a]
        with self.assertRaisesRegex(s.Skip, "monthly"):
            s.guard([], records, candidate(99), NOW)
        s.guard([draft(n + 1) for n in range(9)], records[:-2], candidate(99), NOW)

    def test_scheduled_and_actual_month_both_counted(self):
        ds = [draft(n + 1) for n in range(10)]
        for d in ds:
            d["scheduled_date"] = "2026-08-31T23:59:00Z"
        with self.assertRaisesRegex(s.Skip, "monthly"):
            s.guard(ds, [], candidate(), NOW)


class CandidateTests(unittest.TestCase):
    def github(self, issues, approval_times=None):
        gh = s.GitHub(Mock())

        def get(path):
            if path.startswith("/collaborators/"):
                return {"permission": "write"}
            raise AssertionError(path)

        def pages(path):
            if path.startswith("/issues?"):
                return issues
            if path.endswith("/comments"):
                return []
            n = int(path.split("/")[2])
            return [
                {
                    "event": "labeled",
                    "label": {"name": "social:approved"},
                    "actor": {"login": "owner"},
                    "created_at": (approval_times or {}).get(n, OLD),
                }
            ]

        gh.get = Mock(side_effect=get)
        gh.pages = Mock(side_effect=pages)
        return gh

    def test_priority_and_oldest_approval_not_creation(self):
        issues = [
            issue(
                n,
                ["social:candidate", "social:approved"]
                + ([f"social:p{p}"] if p < 3 else []),
            )
            for n, p in ((1, 3), (2, 2), (3, 1), (4, 0), (5, 0))
        ]
        earlier = (NOW - timedelta(days=4)).isoformat()
        issues[-1]["updated_at"] = earlier
        gh = self.github(issues, {5: earlier})
        self.assertEqual([c["issue"] for c in gh.candidates([])], [5, 4, 3, 2, 1])

    def test_unapproved_scheduled_published_closed_pr_ignored(self):
        issues = [
            issue(1, ["social:candidate"]),
            issue(2, ["social:approved"]),
            issue(3, ["social:candidate", "social:approved", "social:scheduled"]),
            issue(4, ["social:candidate", "social:approved", "social:published"]),
            {**issue(5), "state": "closed"},
            {**issue(6), "pull_request": {}},
        ]
        self.assertEqual(self.github(issues).candidates([]), [])

    def test_edited_after_approval_and_untrusted_approval_ignored(self):
        gh = self.github([{**issue(), "updated_at": NOW.isoformat()}])
        self.assertEqual(gh.candidates([]), [])
        gh = self.github([issue()])
        gh.get = Mock(return_value={"permission": "read"})
        self.assertEqual(gh.candidates([]), [])

    def test_journal_and_candidate_comment_prevent_reselection(self):
        self.assertEqual(self.github([issue()]).candidates([accepted()]), [])
        gh = self.github([issue()])
        orig = gh.pages
        gh.pages = lambda p: (
            [{"body": s.MARKER}] if p.endswith("/comments") else orig(p)
        )
        self.assertEqual(gh.candidates([]), [])

    def test_exact_copy_extraction(self):
        copy = "A tested demo\nwith reproducible inputs"
        self.assertEqual(s.copy_from_body(body(copy)), copy)

    def test_empty_overlength_unicode_and_short_url(self):
        for copy in (
            "",
            "_No response_",
            "a" * 281,
            "界" * 141,
            "a" * 260 + " https://t.co",
            "bad\x00text",
            "a" * 240 + " a.co,b.co",
        ):
            with self.subTest(copy=copy[:10]), self.assertRaises(s.Skip):
                s.copy_from_body(body(copy))
        self.assertEqual(s.copy_from_body(body("a" * 280)), "a" * 280)
        self.assertEqual(s.copy_from_body(body("界" * 140)), "界" * 140)

    def test_missing_duplicate_headings_and_evidence_invalid(self):
        for value in (
            "",
            body() + "\n### Post copy\nOther",
            body().replace("https://github.com", "http://github.com"),
        ):
            with self.assertRaises(s.Skip):
                s.copy_from_body(value)


class RunTests(unittest.TestCase):
    def setUp(self):
        self.gh = MemoryGH()
        self.tf = Mock(set_id=123)
        self.tf.snapshot.return_value = []

        def schedule(c):
            self.gh.events.append("typefully")
            return draft(1234, "scheduled", FUTURE)

        self.tf.schedule.side_effect = schedule

    def run_live(self):
        return s.run(self.gh, self.tf, False, lambda: NOW)

    def test_no_candidate_never_fills_quota(self):
        self.gh.items = []
        self.assertIn("unused", self.run_live())
        self.tf.snapshot.assert_not_called()
        self.tf.schedule.assert_not_called()

    def test_dry_run_has_zero_writes(self):
        self.assertIn("DRY_RUN", s.run(self.gh, self.tf, True, lambda: NOW))
        self.tf.schedule.assert_not_called()
        self.assertEqual(self.gh.events, [])

    def test_success_only_then_mutates_candidate_and_one_per_run(self):
        self.gh.items += [candidate(2)]
        self.assertIn("SCHEDULED", self.run_live())
        self.assertEqual(
            self.gh.events, ["reserved", "typefully", "accepted", "finish"]
        )
        self.assertEqual(self.gh.finished, [1])
        self.tf.schedule.assert_called_once()

    def test_failures_leave_candidate_unmodified_and_reservation_blocks_retry(self):
        for error in (
            s.Skip("SKIP: HTTP 400"),
            s.Skip("SKIP: HTTP 429"),
            s.Skip("SKIP: HTTP 500"),
            TimeoutError(),
            ValueError("malformed"),
        ):
            with self.subTest(error=type(error).__name__):
                self.setUp()
                self.tf.schedule.side_effect = error
                with self.assertRaises(Exception):
                    self.run_live()
                self.assertEqual(self.gh.finished, [])
                self.assertEqual(self.gh.items, [candidate()])
                self.gh.items += [candidate(2)]
                with self.assertRaisesRegex(s.Skip, "unresolved"):
                    self.run_live()
                self.tf.schedule.assert_called_once()

    def test_crash_after_success_before_candidate_update_cannot_duplicate(self):
        self.gh.fail_finish = True
        with self.assertRaises(s.Skip):
            self.run_live()
        self.gh.fail_finish = False
        self.assertIn("no valid", self.run_live())
        self.tf.schedule.assert_called_once()

    def test_crash_before_acceptance_journal_globally_halts(self):
        append = self.gh.append

        def fail(record):
            if record["kind"] == "accepted":
                raise s.Skip("SKIP: journal lost connection")
            append(record)

        self.gh.append = fail
        with self.assertRaises(s.Skip):
            self.run_live()
        with self.assertRaisesRegex(s.Skip, "unresolved"):
            self.run_live()
        self.tf.schedule.assert_called_once()
        self.assertEqual(self.gh.finished, [])

    def test_reservation_write_failure_never_calls_typefully(self):
        self.gh.fail_append = True
        with self.assertRaises(s.Skip):
            self.run_live()
        self.tf.schedule.assert_not_called()

    def test_changed_snapshot_or_approval_never_writes(self):
        self.tf.snapshot.side_effect = [[], [draft()]]
        with self.assertRaises(s.Skip):
            self.run_live()
        self.assertEqual(self.gh.events, [])
        self.tf.schedule.assert_not_called()
        self.setUp()
        self.gh.candidates = Mock(side_effect=[[candidate()], []])
        with self.assertRaises(s.Skip):
            self.run_live()
        self.assertEqual(self.gh.events, [])

    def test_malformed_success_does_not_complete(self):
        for result in (
            {},
            [],
            None,
            draft(2, "draft"),
            {**draft(2, "scheduled", FUTURE), "social_set_id": 999},
        ):
            self.setUp()
            self.tf.schedule.side_effect = None
            self.tf.schedule.return_value = result
            with self.assertRaises(s.Skip):
                self.run_live()
            self.assertEqual(self.gh.finished, [])

    def test_standard_post_response_defaults_accepted(self):
        d = draft(1234, "scheduled", FUTURE)
        d["platforms"]["x"]["posts"][0].update(
            media_ids=[], quote_post_url=None, paid_partnership=False
        )
        record = s.accepted_record(d, candidate(), 123, NOW)
        self.assertEqual(record["draft_id"], 1234)

    def test_success_next_execution_no_duplicate_even_after_labels_removed(self):
        self.run_live()
        self.assertIn("no valid", self.run_live())
        self.tf.schedule.assert_called_once()


class TransportTests(unittest.TestCase):
    def test_journal_requires_lock_and_complete_comment_inventory(self):
        gh = s.GitHub(Mock())
        gh.get = Mock(
            return_value={
                "body": s.LEDGER_MARKER,
                "locked": True,
                "state": "open",
                "comments": 0,
            }
        )
        gh.pages = Mock(return_value=[])
        self.assertEqual(gh.journal(), [])
        for change in ({"comments": 1}, {"locked": False}, {"state": "closed"}):
            gh.get.return_value = {
                "body": s.LEDGER_MARKER,
                "locked": True,
                "state": "open",
                "comments": 0,
                **change,
            }
            with self.assertRaises(s.Skip):
                gh.journal()

    def test_unexpected_failure_never_logs_exception_or_response_secrets(self):
        env = {
            "TYPEFULLY_API_KEY": "sensitive-key",
            "TYPEFULLY_SOCIAL_SET_ID": "987654321",
            "GH_TOKEN": "sensitive-token",
            "TYPEFULLY_QUEUE_READY": "true",
            "GITHUB_REPOSITORY": s.REPO,
        }
        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(s, "run", side_effect=RuntimeError("sensitive-key 987654321")),
            patch("sys.stdout", new_callable=io.StringIO) as output,
        ):
            self.assertEqual(s.main(["--dry-run"]), 1)
            self.assertNotIn("sensitive", output.getvalue())
            self.assertNotIn("987654321", output.getvalue())

    def test_secret_in_candidate_never_reaches_any_write(self):
        gh, tf = MemoryGH(), Mock()
        with (
            patch.dict(os.environ, {"TYPEFULLY_API_KEY": "reproducible"}),
            self.assertRaisesRegex(s.Skip, "secret material"),
        ):
            s.run(gh, tf, False, lambda: NOW)
        self.assertEqual(gh.events, [])
        tf.snapshot.assert_not_called()

    def test_missing_queue_confirmation_never_reaches_network(self):
        env = {
            "TYPEFULLY_API_KEY": "secret",
            "TYPEFULLY_SOCIAL_SET_ID": "123",
            "GH_TOKEN": "secret",
        }
        with (
            patch.dict(os.environ, env, clear=True),
            patch.object(s.HTTP, "request") as request,
            patch("sys.stdout", new_callable=io.StringIO) as output,
        ):
            s.main([])
            request.assert_not_called()
            self.assertIn("TYPEFULLY_QUEUE_READY", output.getvalue())

    def test_twelve_serial_attempts_only_schedule_ten_even_if_drafts_disappear(self):
        gh = MemoryGH()
        gh.items = [candidate(n) for n in range(1, 13)]
        tf = Mock(set_id=123)
        tf.snapshot.return_value = []
        now = datetime(2026, 9, 1, 12, tzinfo=s.UTC)
        tf.schedule.side_effect = lambda c: draft(
            c["issue"], "scheduled", (now + timedelta(hours=1)).isoformat()
        )
        for n in range(12):
            now = datetime(2026, 9, 1, 12, tzinfo=s.UTC) + timedelta(hours=48 * n)
            if n < 10:
                self.assertIn("SCHEDULED", s.run(gh, tf, False, lambda: now))
            else:
                with self.assertRaisesRegex(s.Skip, "monthly"):
                    s.run(gh, tf, False, lambda: now)
        self.assertEqual(tf.schedule.call_count, 10)
        self.assertEqual(len(gh.finished), 10)

    def test_transport_blocks_every_dry_run_write_before_io(self):
        http = s.HTTP("https://api.typefully.com", "secret", True)
        http.opener = Mock()
        for method in ("POST", "PATCH", "DELETE", "PUT"):
            with self.assertRaisesRegex(s.Skip, "dry-run"):
                http.request(method, "/v2/example", {})
        http.opener.open.assert_not_called()

    def test_errors_timeout_malformed_rate_limit_are_sanitized(self):
        for error in (
            urllib.error.HTTPError("secret", 429, "secret", {}, None),
            urllib.error.HTTPError("secret", 500, "secret", {}, None),
            TimeoutError("secret"),
        ):
            http = s.HTTP("https://api.typefully.com", "secret", False)
            http.opener = Mock()
            http.opener.open.side_effect = error
            with self.assertRaises(s.Skip) as caught:
                http.request("POST", "/v2/example", {})
            self.assertNotIn("secret", str(caught.exception))
            http.opener.open.assert_called_once()
        http.opener.open.side_effect = None
        http.opener.open.return_value.__enter__ = Mock(
            return_value=Mock(status=200, read=Mock(return_value=b"not json secret"))
        )
        http.opener.open.return_value.__exit__ = Mock(return_value=False)
        with self.assertRaisesRegex(s.Skip, "JSON"):
            http.request("GET", "/v2/example")

    def test_redirect_is_never_followed(self):
        with self.assertRaises(s.Skip):
            s.NoRedirect().redirect_request(
                None, None, 302, "", {}, "https://evil.example"
            )

    def test_payload_is_single_x_post_and_next_free_slot(self):
        http = Mock()
        s.Typefully(http, "123").schedule(candidate())
        method, path, payload = http.request.call_args.args
        self.assertEqual((method, path), ("POST", "/v2/social-sets/123/drafts"))
        self.assertEqual(payload["publish_at"], "next-free-slot")
        self.assertEqual(
            payload["platforms"],
            {"x": {"enabled": True, "posts": [{"text": candidate()["copy"]}]}},
        )

    def snapshot_http(self, count=0):
        http = Mock()

        def request(method, path, data=None):
            self.assertEqual(method, "GET")
            if path.endswith("/123/"):
                return {"id": 123, "platforms": {"x": {"username": "entrotterxyz"}}}
            if "?" in path:
                offset = int(path.split("offset=")[1].split("&")[0])
                rows = [draft(n + 1) for n in range(offset, min(offset + 50, count))]
                return {
                    "results": rows,
                    "count": count,
                    "limit": 50,
                    "offset": offset,
                    "next": "https://untrusted.example"
                    if offset + 50 < count
                    else None,
                }
            return draft(int(path.rsplit("/", 1)[1]))

        http.request.side_effect = request
        return http

    def test_pagination_all_pages_and_untrusted_next_url_not_followed(self):
        http = self.snapshot_http(51)
        self.assertEqual(len(s.Typefully(http, "123").snapshot()), 51)
        self.assertTrue(
            all(
                c.args[1].startswith("/v2/social-sets/123/")
                for c in http.request.call_args_list
            )
        )

    def test_bad_pagination_and_wrong_account_fail_closed(self):
        for bad in (
            {"results": [], "count": 10, "limit": 50, "offset": 0, "next": None},
            {"results": [], "count": 0, "limit": 50, "offset": 0},
            [],
        ):
            http = self.snapshot_http()
            original = http.request.side_effect
            http.request.side_effect = lambda m, p, d=None: (
                bad if "?" in p else original(m, p, d)
            )
            with self.assertRaises(s.Skip):
                s.Typefully(http, "123").snapshot()
        http = Mock()
        http.request.return_value = {
            "id": 123,
            "platforms": {"x": {"username": "other"}},
        }
        with self.assertRaisesRegex(s.Skip, "approved X account"):
            s.Typefully(http, "123").snapshot()

    def test_journal_malformed_forged_or_unresolved_halts(self):
        for comments in (
            [comment(reservation())],
            [{"body": s.MARKER + "oops", "user": {"login": "github-actions[bot]"}}],
            [{**comment(reservation()), "user": {"login": "attacker"}}],
            [comment(accepted())],
            [comment(reservation()), comment(reservation())],
        ):
            with self.assertRaises(s.Skip):
                s.parse_journal(comments)
        self.assertEqual(
            len(s.parse_journal([comment(reservation()), comment(accepted())])), 2
        )

    def test_missing_credentials_no_network_and_human_blocked_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            summary = Path(directory) / "summary"
            with (
                patch.dict(
                    os.environ, {"GITHUB_STEP_SUMMARY": str(summary)}, clear=True
                ),
                patch.object(s.HTTP, "request") as request,
                patch("sys.stdout", new_callable=io.StringIO) as out,
            ):
                self.assertEqual(s.main([]), 0)
                request.assert_not_called()
                self.assertIn("HUMAN_BLOCKED", out.getvalue())
                self.assertIn("HUMAN_BLOCKED", summary.read_text())

    def test_live_ref_and_repository_guard_no_network(self):
        for repo, ref in (
            ("fork/repo", "refs/heads/main"),
            (s.REPO, "refs/heads/feature"),
        ):
            with (
                patch.dict(
                    os.environ,
                    {
                        "TYPEFULLY_API_KEY": "secret",
                        "TYPEFULLY_SOCIAL_SET_ID": "123",
                        "GH_TOKEN": "secret",
                        "GITHUB_REPOSITORY": repo,
                        "GITHUB_REF": ref,
                        "GITHUB_ACTIONS": "true",
                        "TYPEFULLY_QUEUE_READY": "true",
                        "GITHUB_EVENT_NAME": "workflow_dispatch",
                    },
                    clear=True,
                ),
                patch.object(s.HTTP, "request") as request,
                patch("sys.stdout", new_callable=io.StringIO) as out,
            ):
                s.main([])
                request.assert_not_called()
                self.assertNotIn("secret", out.getvalue())


if __name__ == "__main__":
    unittest.main()
