# Selective X publishing

Entrotter uses GitHub Issues as a curated editorial queue for **@entrotterxyz**.
Ten posts per UTC calendar month is a hard ceiling, never a target. No commit,
release, dependency update or CI event creates or approves a post. There is no
runtime LLM, direct X API, X browser automation, or paid automation service.

## Editorial review

Use the **Social post candidate** issue form. Its five fixed headings separate
exact post copy, rationale, one public HTTPS evidence URL, preferred timing and
notes. Only the copy is sent to X. Preserve the headings, including optional ones.

Spend a slot on a meaningful release, working demo, major visible capability,
reproducibility milestone, useful technical result/tutorial, significant hackathon
milestone, contributor opportunity or architecture insight. Reject routine commits,
formatting, CI/dependency/typo fixes, internal refactors, trivial README changes,
generic motivation and repeated promotion. Never invent metrics, adoption,
benchmarks, partnerships, prizes, deployments or results. Distinguish a tested
review branch from a merged release or live deployment. The maintainer must
inspect the evidence and rights to publish; code cannot verify the truth of prose.

Prefer concise, technically precise English useful to developers/researchers,
a single post and at most one relevant link. There is no thread splitting.
The stdlib length check deliberately overestimates X's 280-character weighting:
ASCII costs one, other Unicode scalars two, and every potential URL separator
(period, internationalized period or `://`) adds 23. This deliberately also
charges punctuation and safely bounds adjacent URLs without whitespace. It can
reject a valid near-limit post, including complex emoji and shortened long URLs;
shorten the copy instead of bypassing it. Controls and empty copy are rejected.

Both `social:candidate` and `social:approved` must be present. A repository
maintainer with write/maintain/admin permission must add approval **last**, after
reviewing copy, evidence, priority and timing. Any subsequent issue update requires
removing and re-adding approval. Do not edit an approved issue, including within
the same second as approval (GitHub REST timestamps have second precision).
Keep approval off until timing is suitable; the optional timing field is a note,
not a scheduling instruction. Priority is P0, P1, P2, then no label; ties use the
oldest current approval event, then issue number. Multiple priority labels use
the highest. A malformed candidate conservatively stops that run for correction.

## Owner setup

1. Connect **@entrotterxyz** to Typefully. Use its dedicated social set; the script
   verifies the connected X username before scheduling.
2. In Typefully **Settings → API**, create a Public API v2 key with read and
   publishing access. Do not reuse a v1 key.
3. Privately call `GET https://api.typefully.com/v2/social-sets` with
   `Authorization: Bearer TYPEFULLY_API_KEY` and identify the Entrotter set.
   Do not paste the response into public logs: it contains social-set identifiers.
4. Store `TYPEFULLY_API_KEY` under repository **Settings → Secrets and variables →
   Actions → Secrets** in `entrotter/entrotter`.
5. Store the numeric `TYPEFULLY_SOCIAL_SET_ID` there as a second **secret**.
6. Configure Typefully posting queue slots / Natural Posting Time. Disable
   **Auto-Plug and Auto-Retweet**: the create endpoint applies account defaults,
   and those extra posts are outside this publisher's control. Use this workflow
   as the sole scheduling writer, keep the social set/account exclusively for this
   queue, and avoid manual rescheduling, deletion, extra posts or other automation.
   Use UTC for the queue calendar to match the explicit budget convention. Once
   these conditions are set, add repository Actions **variable**
   `TYPEFULLY_QUEUE_READY=true` as the operator's confirmation. It is not a secret.
7. Create a `social:candidate` Issue with the form.
8. Review its exact copy against the linked project evidence.
9. Add a priority label if useful, then add `social:approved` last.
10. After independent PR approval and merge to protected `main`, GitHub Actions
    checks once daily at 09:17 UTC. Typefully chooses the final time using
    `publish_at: "next-free-slot"`. Manual dispatch defaults to **dry-run**.

Never paste either secret into Codex chat, issues, commits, PR descriptions or
logs. Secrets are environment inputs only. Do not enable shell tracing or print
API responses. The program emits only fixed status messages and candidate IDs;
its durable records contain numeric draft IDs, UTC timestamps and copy hashes,
never keys, social-set IDs, private URLs or post copy.

The seven `social:*` labels and locked [journal issue #50](https://github.com/entrotter/entrotter/issues/50)
are provisioned. The script does not create labels/issues at runtime. No candidate
has been approved as part of implementation. If credentials are absent, the step
safely reports `HUMAN_BLOCKED` in `GITHUB_STEP_SUMMARY` without network access.
A Typefully 402/403 response is a safe stop; this tool never upgrades a plan or
spends money. Account/API entitlement must be established in the existing account.

## Budget and at-most-once safety

- A single concurrency group serializes both live and dry runs, with cancellation
  disabled. The live job has contents-read/issues-write permissions; dry-run has
  contents-read/issues-read. Both check out `main` without persisted credentials.
  Fork repositories and non-main live dispatches cannot publish. Tests have no
  Typefully credentials. Do not invoke live mode outside this workflow.
- All draft pages are read, including detail content to count individual posts in
  existing threads and platforms. Pagination inconsistencies, changing snapshots,
  malformed fields, unsupported article content, errors, in-progress publication,
  overdue schedules and transport errors stop publication. Limits on pages, response
  size and request time prevent unbounded reads. Two matching snapshots and a fresh
  GitHub approval/journal read are required immediately before a live reservation.
- The monthly count is a union keyed by draft ID of Typefully state and durable
  accepted journal history. Deleted pipeline drafts still consume their recorded
  capacity. A draft counts in each represented creation/update/scheduled/published
  month, conservatively counting multiple platforms/posts. Current and **all known
  future months** must each have capacity before server-selected `next-free-slot`.
  Past full months expire. This deliberately may skip a usable slot rather than
  guess the server's eventual month. A ten-minute month-boundary window stops writes.
- At most one new post is attempted per run and per 48 hours. The cooldown includes
  successful journal acceptance and Typefully creation/update/publication times;
  manual edits can extend it conservatively. No activity is created to fill quota.
- Before the only Typefully POST, an append-only `reserved` record is written to
  journal #50. Any unresolved reservation halts **all** subsequent live attempts,
  including other candidates and future months. There is no HTTP write retry.
  A crash after request acceptance cannot turn into a duplicate on the next run.
- Only a validated scheduled response for exactly the approved X text permits an
  `accepted` journal record. Then the candidate receives `social:scheduled`, loses
  `social:approved`, and receives a comment with draft ID, acceptance time and
  scheduled time. Candidate labels/comments are untouched on a Typefully failure.
  Its editorial labels remain eligible, but its journal reservation imposes a
  separate safety hold: failure does **not** authorize another automatic attempt.
- Scheduled/published labels, candidate receipt comments, journal entries and
  matching Typefully draft titles independently prevent reselection. Success followed
  by a GitHub update failure remains terminal through the journal. Do not remove
  journal records or reset candidates to force publication.
- Dry-run performs **zero network writes**, enforced at the shared HTTP boundary
  for GitHub and Typefully, not just by avoiding the main scheduling call.

The deterministic ceiling applies to this serialized writer under the configured
exclusive-account conditions. The APIs provide no atomic cross-service transaction
or idempotency key for draft creation. They cannot prevent an owner/other writer
from posting between reads, deleting historical evidence, enabling Auto-Plug, or
moving posts into an already full month. `TYPEFULLY_QUEUE_READY` is an explicit
operator assertion of those conditions, not a claim that the API can verify them.
Do not enable the queue if other writers need to operate concurrently.

## Failure recovery and publication status

A scheduled response is **not** proof of publication. In v1 `social:scheduled` is
the durable terminal state. Reconciliation to `social:published` is a separate
read-only investigation followed by a reviewed label update only when Typefully
confirms successful X publication and provides the resulting X URL. No such
publication is claimed by this implementation.

For an unresolved reservation, disable the workflow and privately inspect the
Typefully draft list/detail for the exact `entrotter/entrotter#NUMBER` internal
title, content hash and timestamps. Never retry POST, delete the reservation, or
copy the candidate into another approved issue merely because a request timed out.
If the draft exists, a separately reviewed maintenance change running as
`github-actions[bot]` can append the verified `accepted` record and finish the
candidate labels/comment. If absence cannot be proven, leave the global hold in
place. v1 deliberately has no automatic reset/abandon/retry switch. Journal entries
from another actor, duplicate reservations or malformed records also require
operator review. Keep the journal locked and preserve its history.

If acceptance was recorded but candidate updates failed, repair only the candidate
receipt/labels from that durable record. Do not send anything to Typefully. Review
all uncertain outcomes against the configured month's budget before resuming.

## Local verification

```bash
python3 -m unittest discover -s tests -p test_social_publish.py -v
python3 -O -m unittest discover -s tests -p test_social_publish.py
python3 scripts/social_publish.py --dry-run
```

The last command reports missing setup unless the relevant environment variables
are configured privately. With credentials it makes GET requests only. Unit tests
mock every Typefully call, including faults and success; no real posting slot is
used. `social-tests.yml` runs them for pull requests and pushes to main. Existing
workspace integration checks remain unchanged; v0.1 contracts are untouched.

The implementation was checked against the [official Typefully v2 API reference](https://typefully.com/docs/api)
and [v1→v2 migration guide](https://support.typefully.com/en/articles/13133296-typefully-api-v1-v2-migration-guide).
See [verification evidence](../evidence/social-publishing/verification.json) for
fresh checks and remaining limits, separately from historical project evidence.
