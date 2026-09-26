# Submission readiness

Status is evidence-backed, not an assertion of eligibility or a prize.

| Gate | Status | Evidence / remaining action |
|---|---|---|
| Track | PASS | Owner explicitly requested Continuity; authenticated Dashboard selected it |
| Registration | PASS | Dashboard says fully confirmed to attend |
| Team membership/facts | PASS | Authenticated team page lists Tomoya Hatanaka; one member |
| New functionality and prior work | PASS | PROVENANCE.md; pre-existing branches and PRs unchanged; additions use existing repositories |
| AI disclosure | PASS | AI_USAGE.md; organizer decides meaningful-contribution eligibility |
| 8 Python + 16 JavaScript tests | PASS | evidence/unit-tests.log, evidence/report-tests.log |
| Real archive execution | PASS | evidence/verified-run.json |
| Fresh reproduction and cleanup | PASS | ../../evidence/tokyo2026/migrated-integration.json; 5 passed, 0 failed/skipped |
| Desktop/mobile/import/keyboard | PASS | evidence/desktop.png, evidence/mobile.png; browser notes pending consolidation |
| Public repository | PASS | engine PR #25, website PR #13 and coordination PR #49 published; current checks pass |
| Public Pages viewer | BLOCKED | Existing-site PR #13 awaits independent approval; temporary repository deletion requested but blocked by missing delete_repo scope |
| New screen recording | PASS | 149-second 1440×1080 captioned silent recording verified and published in existing coordination repo release tokyo-continuity-demo |
| Finalist compliant narration | NOT APPLICABLE | Partner-only path selected; silent walkthrough is supplemental |
| Uniswap FEEDBACK.md | PASS | FEEDBACK.md published on docs/tokyo-continuity |
| Uniswap feedback form | PASS | Visible thank-you confirmation; evidence: ../../evidence/tokyo2026/submission-progress.json |
| English submission text | PASS | SUBMISSION.md reflects actual new evidence and provenance |
| Exact hacking start | PASS | Official schedule: September 25, 2026, 21:00 JST |
| Final entry submission | BLOCKED | Form completion and final readback pending |
| Organizer eligibility acceptance | BLOCKED | No organizer approval claimed; disclosure retained |

Deadline from current official pages: September 27, 2026, 09:00 JST / 00:00 UTC.
Internal target: 08:00 JST. Source and form rules in PROVENANCE.md.

Known failures resolved: default Python RPC User-Agent was rejected; setting an explicit app agent
worked with TLS verification intact. An initial test accidentally replaced the zero/uncomputed local
root with the same value; the test now changes it and rejects divergence. Setup timestamps initially
varied across clean runs; explicit timestamps fixed exact receipt reproduction. Browser test harness
could not construct Buffer inline; a local malformed JSON file verified the same rejection path.

Existing engine regression tests: 80 passed after migration. Viewer regression tests: 10 Python and 13 Node passed. New tests: 8 Python and 16 Node passed. GitHub engine EVM/unit matrix, website check and coordination integration checks passed; website build/deploy correctly skipped on the PR.

ETHGlobal project details, the three existing repository selections, tech stack and AI disclosure are saved. Final submission remains blocked by required image upload; browser extension file access returned Not allowed. No final submission success is claimed.
