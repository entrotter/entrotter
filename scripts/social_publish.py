"""Selective, fail-closed Typefully v2 publisher. No third-party runtime packages."""

import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

REPO = "entrotter/entrotter"
LEDGER = 50
MARKER = "entrotter-social-v1:"
LEDGER_MARKER = "<!-- entrotter-social-ledger-v1 -->"
FIELDS = (
    "Post copy",
    "Why this deserves one of the monthly slots",
    "Evidence/source URL",
    "Preferred timing",
    "Notes",
)
UTC = timezone.utc


class Skip(Exception):
    """Only fixed, credential-free messages may cross the logging boundary."""


def require(condition, reason="SKIP: ambiguous response or state"):
    if not condition:
        raise Skip(reason)


def timestamp(value):
    require(isinstance(value, str))
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise Skip("SKIP: invalid timestamp") from None
    require(result.tzinfo is not None)
    return result.astimezone(UTC)


def positive_id(value):
    require(type(value) is int and value > 0)
    return value


def month(value):
    return value.astimezone(UTC).strftime("%Y-%m")


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def copy_from_body(body):
    require(isinstance(body, str), "SKIP: invalid candidate format")
    sections = re.split(r"^### (.+)\n", body.replace("\r\n", "\n"), flags=re.M)
    require(
        sections[0].strip() == "" and sections[1::2] == list(FIELDS),
        "SKIP: invalid candidate format",
    )
    fields = dict(zip(sections[1::2], (s.strip() for s in sections[2::2])))
    copy = fields["Post copy"]
    require(copy and copy != "_No response_", "SKIP: empty post")
    # Conservative upper bound: every non-ASCII scalar costs two. Each possible
    # URL separator adds 23, even punctuation. This also bounds adjacent URLs with
    # no whitespace, without implementing X's evolving URL/emoji parser.
    require(
        all(
            c == "\n" or (c.isprintable() and not 0xD800 <= ord(c) <= 0xDFFF)
            for c in copy
        ),
        "SKIP: unsupported control character",
    )
    weight = sum(1 if ord(c) < 128 else 2 for c in copy)
    weight += 23 * (
        sum(copy.count(dot) for dot in (".", "。", "．", "｡")) + copy.count("://")
    )
    require(weight <= 280, "SKIP: post exceeds conservative X length limit")
    reason = fields[FIELDS[1]]
    require(reason and reason != "_No response_", "SKIP: missing editorial rationale")
    evidence = urllib.parse.urlsplit(fields[FIELDS[2]])
    require(
        evidence.scheme == "https"
        and evidence.hostname
        and not evidence.username
        and not evidence.password
        and not any(c.isspace() for c in fields[FIELDS[2]]),
        "SKIP: evidence must be a public HTTPS URL",
    )
    return copy


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Skip("SKIP: HTTP redirect refused")


class HTTP:
    def __init__(self, base, token, dry_run):
        self.base = base
        self.token = token
        self.dry_run = dry_run
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, method, path, data=None):
        require(path.startswith("/") and not path.startswith("//"))
        require(not self.dry_run or method == "GET", "SKIP: dry-run forbids all writes")
        request = urllib.request.Request(
            self.base + path,
            method=method,
            data=None if data is None else json.dumps(data).encode(),
            headers={
                "Authorization": "Bearer " + self.token,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "entrotter-social-v1",
            },
        )
        try:
            with self.opener.open(request, timeout=20) as response:
                require(200 <= response.status < 300)
                raw = response.read(2_000_001)
                require(len(raw) <= 2_000_000, "SKIP: oversized API response")
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as error:
            # Never print URLs, bodies, headers, request objects or exception text.
            raise Skip("SKIP: API returned HTTP " + str(error.code)) from None
        except (OSError, ValueError, TimeoutError):
            raise Skip("SKIP: API transport or JSON failure; no retry") from None


class GitHub:
    def __init__(self, http):
        self.http = http
        self.root = "/repos/" + REPO

    def get(self, path):
        return self.http.request("GET", self.root + path)

    def pages(self, path):
        items = []
        for page in range(1, 101):
            sep = "&" if "?" in path else "?"
            batch = self.get(f"{path}{sep}per_page=100&page={page}")
            require(isinstance(batch, list) and all(isinstance(i, dict) for i in batch))
            items.extend(batch)
            if len(batch) < 100:
                return items
        raise Skip("SKIP: GitHub pagination bound reached")

    def comment(self, issue, body):
        result = self.http.request(
            "POST", f"{self.root}/issues/{issue}/comments", {"body": body}
        )
        require(isinstance(result, dict) and result.get("body") == body)
        positive_id(result.get("id"))

    def journal(self):
        issue = self.get(f"/issues/{LEDGER}")
        require(
            isinstance(issue, dict)
            and LEDGER_MARKER in issue.get("body", "")
            and issue.get("locked") is True
            and issue.get("state") == "open",
            "SKIP: durable journal missing; never recreate automatically",
        )
        comments = self.pages(f"/issues/{LEDGER}/comments")
        require(
            type(issue.get("comments")) is int and len(comments) == issue["comments"],
            "SKIP: journal comment count changed or incomplete",
        )
        return parse_journal(comments)

    def append(self, record):
        self.comment(LEDGER, MARKER + json.dumps(record, sort_keys=True))

    def candidates(self, records):
        blocked = {r["issue"] for r in records}
        candidates = []
        for issue in self.pages(
            "/issues?state=open&labels=social%3Acandidate,social%3Aapproved"
        ):
            if "pull_request" in issue:
                continue
            number = positive_id(issue.get("number"))
            if number in blocked or not eligible(issue):
                continue
            comments = self.pages(f"/issues/{number}/comments")
            if any(MARKER in str(c.get("body", "")) for c in comments):
                continue
            events = self.pages(f"/issues/{number}/events")
            approvals = [
                e
                for e in events
                if e.get("event") == "labeled"
                and e.get("label", {}).get("name") == "social:approved"
            ]
            if not approvals:
                continue
            approval = max(approvals, key=lambda e: timestamp(e.get("created_at")))
            approved_at = timestamp(approval.get("created_at"))
            # Editing copy or metadata after approval requires remove/re-add approval.
            if timestamp(issue.get("updated_at")) > approved_at:
                continue
            login = approval.get("actor", {}).get("login", "")
            require(isinstance(login, str) and re.fullmatch(r"[A-Za-z0-9-]+", login))
            permission = self.get(f"/collaborators/{login}/permission")
            require(isinstance(permission, dict))
            if permission.get("permission") not in {"admin", "maintain", "write"}:
                continue
            copy = copy_from_body(issue.get("body"))
            candidates.append(
                {
                    "issue": number,
                    "copy": copy,
                    "body": issue["body"],
                    "updated_at": issue["updated_at"],
                    "approved_at": approved_at,
                    "priority": priority(issue),
                }
            )
        return sorted(
            candidates, key=lambda c: (c["priority"], c["approved_at"], c["issue"])
        )

    def finish(self, number, accepted):
        self.http.request(
            "POST",
            f"{self.root}/issues/{number}/labels",
            {"labels": ["social:scheduled"]},
        )
        self.http.request(
            "DELETE", f"{self.root}/issues/{number}/labels/social%3Aapproved"
        )
        self.comment(number, MARKER + json.dumps(accepted, sort_keys=True))


def eligible(issue):
    labels = {label["name"] for label in issue["labels"]}
    return (
        issue.get("state") == "open"
        and {"social:candidate", "social:approved"} <= labels
        and not {"social:scheduled", "social:published"} & labels
    )


def priority(issue):
    labels = {label["name"] for label in issue["labels"]}
    return next((i for i in range(3) if f"social:p{i}" in labels), 3)


def parse_journal(comments):
    records = []
    reserved = {}
    accepted = set()
    for comment in comments:
        body = comment.get("body", "")
        require(isinstance(body, str))
        if MARKER not in body:
            continue
        require(
            body.startswith(MARKER)
            and comment.get("user", {}).get("login") == "github-actions[bot]",
            "SKIP: journal integrity requires operator review",
        )
        try:
            record = json.loads(body[len(MARKER) :])
        except ValueError:
            raise Skip("SKIP: malformed journal") from None
        require(isinstance(record, dict))
        number = positive_id(record.get("issue"))
        timestamp(record.get("at"))
        require(re.fullmatch(r"[0-9a-f]{64}", record.get("copy_sha256", "")))
        if record.get("kind") == "reserved":
            require(number not in reserved)
            reserved[number] = record
        elif record.get("kind") == "accepted":
            require(number in reserved and number not in accepted)
            require(record["copy_sha256"] == reserved[number]["copy_sha256"])
            require(timestamp(record["at"]) >= timestamp(reserved[number]["at"]))
            positive_id(record.get("draft_id"))
            timestamp(record.get("scheduled_date"))
            accepted.add(number)
        else:
            raise Skip("SKIP: unknown journal record")
        records.append(record)
    require(
        set(reserved) == accepted,
        "SKIP: unresolved write reservation; operator reconciliation required",
    )
    require(
        len({r["draft_id"] for r in records if r["kind"] == "accepted"})
        == len(accepted)
    )
    return records


class Typefully:
    def __init__(self, http, social_set_id):
        require(
            re.fullmatch(r"[1-9][0-9]*", social_set_id), "SKIP: invalid configuration"
        )
        self.http = http
        self.set_id = int(social_set_id)
        self.root = f"/v2/social-sets/{social_set_id}"

    def snapshot(self):
        account = self.http.request("GET", self.root + "/")
        require(isinstance(account, dict) and account.get("id") == self.set_id)
        require(
            account.get("platforms", {}).get("x", {}).get("username", "").lower()
            == "entrotterxyz",
            "SKIP: social set is not the approved X account",
        )
        quota = account.get("publishing_quota")
        if quota is not None:
            require(isinstance(quota, dict))
            remaining = quota.get("remaining")
            require(
                remaining == "unlimited" or (type(remaining) is int and remaining > 0),
                "SKIP: Typefully account quota exhausted or unknown",
            )
        summaries = []
        count = None
        for offset in range(0, 5000, 50):
            page = self.http.request(
                "GET",
                f"{self.root}/drafts?limit=50&offset={offset}&order_by=created_at",
            )
            require(isinstance(page, dict) and isinstance(page.get("results"), list))
            require(type(page.get("count")) is int and page["count"] >= 0)
            if count is None:
                count = page["count"]
            require(
                page["count"] == count
                and page.get("offset") == offset
                and page.get("limit") == 50
            )
            batch = page["results"]
            require(len(batch) == min(50, count - offset))
            summaries.extend(batch)
            if len(summaries) == count:
                require("next" in page and page["next"] is None)
                break
            require(isinstance(page.get("next"), str) and page["next"])
        else:
            raise Skip("SKIP: Typefully pagination bound reached")
        drafts = []
        seen = set()
        for row in summaries:
            require(isinstance(row, dict))
            number = positive_id(row.get("id"))
            require(number not in seen)
            seen.add(number)
            detail = self.http.request("GET", f"{self.root}/drafts/{number}")
            require(
                isinstance(detail, dict)
                and detail.get("id") == number
                and detail.get("social_set_id") == self.set_id
                and detail.get("status") == row.get("status")
                and detail.get("updated_at") == row.get("updated_at")
            )
            drafts.append(detail)
        return drafts

    def schedule(self, candidate):
        return self.http.request(
            "POST",
            self.root + "/drafts",
            {
                "platforms": {
                    "x": {"enabled": True, "posts": [{"text": candidate["copy"]}]}
                },
                "publish_at": "next-free-slot",
                "draft_title": f"entrotter/entrotter#{candidate['issue']}",
            },
        )


def draft_weight(draft):
    platforms = draft.get("platforms")
    require(isinstance(platforms, dict))
    weight = 0
    for name, platform in platforms.items():
        if platform is None:
            continue
        require(isinstance(platform, dict))
        if name == "x_article":
            raise Skip("SKIP: X Article quota is not supported")
        require(type(platform.get("enabled")) is bool)
        if platform["enabled"]:
            posts = platform.get("posts")
            require(
                isinstance(posts, list)
                and posts
                and all(isinstance(p, dict) for p in posts)
            )
            weight += len(posts)
    require(weight > 0)
    return weight


def guard(drafts, records, candidate, now):
    require(now.tzinfo is not None)
    counts: dict[str, dict[int, int]] = defaultdict(dict)
    recent = []
    seen = set()
    for draft in drafts:
        number = positive_id(draft.get("id"))
        require(number not in seen)
        seen.add(number)
        require(
            draft.get("draft_title") != f"entrotter/entrotter#{candidate['issue']}",
            "SKIP: candidate already exists in Typefully",
        )
        state = draft.get("status")
        require(
            state in {"draft", "planned", "scheduled", "published"}
            and draft.get("publish_state") in {None, "finished"},
            "SKIP: ambiguous Typefully publishing state",
        )
        if state in {"draft", "planned"}:
            require(
                draft.get("published_at") is None and draft.get("publish_state") is None
            )
            continue
        dates = [timestamp(draft.get("created_at"))]
        if draft.get("updated_at") is not None:
            dates.append(timestamp(draft["updated_at"]))
        recent.extend(dates)
        if draft.get("scheduled_date") is not None:
            scheduled = timestamp(draft["scheduled_date"])
            dates.append(scheduled)
            if state == "scheduled":
                require(scheduled > now, "SKIP: overdue scheduled draft")
        else:
            require(state == "published")
        if state == "published":
            published = timestamp(draft.get("published_at"))
            require(published <= now)
            dates.append(published)
            recent.append(published)
        weight = draft_weight(draft)
        for date in dates:
            counts[month(date)][number] = weight
    reservations = {r["issue"]: r for r in records if r["kind"] == "reserved"}
    for record in records:
        require(
            record["issue"] != candidate["issue"], "SKIP: candidate already attempted"
        )
        if record["kind"] != "accepted":
            continue
        number = record["draft_id"]
        at = timestamp(record["at"])
        recent.append(at)
        dates = [
            at,
            timestamp(reservations[record["issue"]]["at"]),
            timestamp(record["scheduled_date"]),
        ]
        for date in dates:
            counts[month(date)][number] = max(1, counts[month(date)].get(number, 0))
    require(
        all(now - date >= timedelta(hours=48) for date in recent),
        "SKIP: 48-hour cooldown",
    )
    # next-free-slot is server-selected. Reserve capacity in EVERY represented
    # current/future month, not an assumed next-slot month. Unknown months are empty.
    require(
        all(
            sum(entries.values()) < 10
            for key, entries in counts.items()
            if key >= month(now)
        ),
        "SKIP: monthly maximum reached",
    )
    require(
        month(now) == month(now + timedelta(minutes=10)),
        "SKIP: month-boundary safety window",
    )


def accepted_record(result, candidate, set_id, now):
    require(isinstance(result, dict) and result.get("social_set_id") == set_id)
    number = positive_id(result.get("id"))
    require(
        result.get("status") == "scheduled" and result.get("publish_state") is None,
        "SKIP: scheduling acceptance is ambiguous; reservation retained",
    )
    scheduled = timestamp(result.get("scheduled_date"))
    require(scheduled > now and draft_weight(result) == 1)
    x = result["platforms"].get("x", {})
    require(x.get("enabled") is True and len(x.get("posts", [])) == 1)
    post = x["posts"][0]
    require(
        post.get("text") == candidate["copy"]
        and not post.get("media_ids")
        and not post.get("quote_post_url")
    )
    return {
        "kind": "accepted",
        "issue": candidate["issue"],
        "at": now.isoformat(),
        "copy_sha256": digest(candidate["copy"]),
        "draft_id": number,
        "scheduled_date": scheduled.isoformat(),
        "result": "scheduled",
    }


def run(gh, tf, dry_run, clock=lambda: datetime.now(UTC)):
    records = gh.journal()
    candidates = gh.candidates(records)
    if not candidates:
        return "SKIP: no valid approved candidates; unused quota stays unused"
    candidate = candidates[0]
    require(
        all(
            not value or value not in candidate["body"]
            for value in (
                os.environ.get(name, "")
                for name in ("TYPEFULLY_API_KEY", "TYPEFULLY_SOCIAL_SET_ID", "GH_TOKEN")
            )
        ),
        "SKIP: candidate contains configured secret material",
    )
    drafts = tf.snapshot()
    guard(drafts, records, candidate, clock())
    if dry_run:
        return f"DRY_RUN: candidate #{candidate['issue']} passes; zero network writes"
    # Refuse a changing snapshot and re-read approval immediately before reserving.
    require(tf.snapshot() == drafts, "SKIP: Typefully state changed during preflight")
    require(gh.journal() == records, "SKIP: journal changed during preflight")
    fresh = gh.candidates(records)
    require(fresh and fresh[0] == candidate, "SKIP: approval or candidate changed")
    now = clock()
    guard(drafts, records, candidate, now)
    gh.append(
        {
            "kind": "reserved",
            "issue": candidate["issue"],
            "at": now.isoformat(),
            "copy_sha256": digest(candidate["copy"]),
        }
    )
    # Exactly ONE attempt. An exception, crash or partial GitHub update can never
    # authorize another attempt, because the durable journal is checked first.
    result = tf.schedule(candidate)
    accepted = accepted_record(result, candidate, tf.set_id, clock())
    gh.append(accepted)
    gh.finish(candidate["issue"], accepted)
    return f"SCHEDULED: candidate #{candidate['issue']}; Typefully accepted; publication unverified"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="GET requests only")
    args = parser.parse_args(argv)
    key = os.environ.get("TYPEFULLY_API_KEY", "")
    social_set = os.environ.get("TYPEFULLY_SOCIAL_SET_ID", "")
    token = os.environ.get("GH_TOKEN", "")
    result = "HUMAN_BLOCKED: connect @entrotterxyz to Typefully; add TYPEFULLY_API_KEY; add TYPEFULLY_SOCIAL_SET_ID; configure the Typefully posting queue; approve the first social:candidate"
    code = 0
    if key and social_set:
        try:
            require(token, "SKIP: missing GitHub token")
            require(
                os.environ.get("TYPEFULLY_QUEUE_READY") == "true",
                "HUMAN_BLOCKED: configure the Typefully posting queue and confirm TYPEFULLY_QUEUE_READY",
            )
            require(
                os.environ.get("GITHUB_REPOSITORY") == REPO, "SKIP: wrong repository"
            )
            if not args.dry_run:
                require(
                    os.environ.get("GITHUB_ACTIONS") == "true"
                    and os.environ.get("GITHUB_REF") == "refs/heads/main"
                    and os.environ.get("GITHUB_EVENT_NAME")
                    in {"schedule", "workflow_dispatch"},
                    "SKIP: live writes require the serialized main-branch workflow",
                )
            gh = GitHub(HTTP("https://api.github.com", token, args.dry_run))
            tf = Typefully(
                HTTP("https://api.typefully.com", key, args.dry_run), social_set
            )
            result = run(gh, tf, args.dry_run)
        except Skip as error:
            result = str(error)
        except Exception:
            # Unexpected data must not print a traceback containing a secret.
            result = "SKIP: unexpected state; inspect privately; no automatic retry"
            code = 1
    print(result)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a", encoding="utf-8") as stream:
            stream.write(result + "\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
