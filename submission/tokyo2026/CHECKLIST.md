# Submission readiness

Status is evidence-backed, not an assertion of eligibility or a prize.

| Gate | Status | Evidence / remaining action |
|---|---|---|
| Track | PASS | Owner explicitly requested Continuity; authenticated Dashboard selected it |
| Registration | PASS | Dashboard says fully confirmed to attend |
| Team membership/facts | BLOCKED | Inspect actual team state; do not infer from Colosseum |
| New functionality and prior work | PASS | PROVENANCE.md; old six repositories unchanged |
| AI disclosure | PASS | AI_USAGE.md; organizer decides meaningful-contribution eligibility |
| 8 Python + 16 JavaScript tests | PASS | evidence/unit-tests.log, evidence/report-tests.log |
| Real archive execution | PASS | evidence/verified-run.json |
| Fresh reproduction and cleanup | PASS | evidence/integration.json; 5 passed, 0 failed/skipped |
| Desktop/mobile/import/keyboard | PASS | evidence/desktop.png, evidence/mobile.png; browser notes pending consolidation |
| Public repository | BLOCKED | Moved to existing repositories; review-branch publication in progress |
| Public Pages viewer | BLOCKED | Temporary separate-repo deployment was verified, then withdrawn by owner request; existing-site PR awaits independent approval |
| New screen recording | BLOCKED | 149-second 1440×1080 captioned silent recording verified; copied into existing coordination workspace |
| Finalist compliant narration | NOT APPLICABLE | Partner-only path selected; silent walkthrough is supplemental |
| Uniswap FEEDBACK.md | PASS | FEEDBACK.md prepared; publication verification pending |
| Uniswap feedback form | BLOCKED | Draft exists, submission not yet confirmed |
| English submission text | PASS | SUBMISSION.md reflects actual new evidence and provenance |
| Exact hacking start | BLOCKED | Schedule still needs verification |
| Final entry submission | BLOCKED | Form completion and final readback pending |
| Organizer eligibility acceptance | BLOCKED | No organizer approval claimed; disclosure retained |

Deadline from current official pages: September 27, 2026, 09:00 JST / 00:00 UTC.
Internal target: 08:00 JST. Source and form rules in PROVENANCE.md.

Known failures resolved: default Python RPC User-Agent was rejected; setting an explicit app agent
worked with TLS verification intact. An initial test accidentally replaced the zero/uncomputed local
root with the same value; the test now changes it and rejects divergence. Setup timestamps initially
varied across clean runs; explicit timestamps fixed exact receipt reproduction. Browser test harness
could not construct Buffer inline; a local malformed JSON file verified the same rejection path.
