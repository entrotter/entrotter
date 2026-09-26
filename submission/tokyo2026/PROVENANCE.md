# Provenance and eligibility

Provenance audit clock reading: 2026-09-26 11:32:15 UTC. First recorded implementation-history commit: 2026-09-26 13:04:48 UTC (22:04:48 JST).
Initial selection: Start from Scratch. The owner subsequently explicitly requested **Continuity Track** in this session. The authenticated Dashboard was read back with Continuity Track selected; no additional toggle was necessary. Organizer acceptance of the final submission remains unconfirmed.

The owner already developed the Entrotter concept and a separate Colosseum product before Tokyo.
The assistant has seen that product's documentation and goal; this is **not a certified clean-room process**.
The Tokyo addition is a newly authored, narrower implementation within existing repositories. No prior engine, SDK, CLI, schemas,
reports, frontend, mascot, video or detailed source implementation is imported.
Anvil/Cast, Python, browser tooling and FFmpeg are general-purpose tools, not project artifacts.
Public protocol addresses and ABI definitions come from Uniswap primary documentation.

## Initial workspace audit (2026-09-26)
Six direct repositories plus four registered worktrees were clean. Local branches, remote branches,
and organization repository list contained no Tokyo-specific implementation. No recent coordination
commits since September 24 were found. Scope: this workspace and the entrotter GitHub organization;
this does not prove the absence of work elsewhere.

| Existing repository | Active branch | HEAD |
|---|---|---|
| entrotter | docs/reproducible-quick-start | 6eb5bc624d884e39efff9bc1444c6a6f590b14fa |
| engine | feat/causal-agent-record-replay | bb8b3e8d32c7cbd49629d337758f30bfdf805045 |
| sdk-python | ci/python-quality-gates | b0c2ba3bba411e548af44101ae06e879bd7b5dc0 |
| cli | ci/python-quality-gates | aba6a6147b2b4b96facf758f9b95b63d8e6b5952 |
| scenarios | feat/historical-agent-cases | 5b718984ac67b8fb49e02f4dab676ae212d2aa58 |
| entrotter.github.io | ci/website-quality | 61740312f281f7e911e0eb6e9482a3c372cb1fae |

PR entrotter#47 and engine#22, sdk-python#6, cli#9, scenarios#8, entrotter.github.io#11
were freshly checked: all OPEN, unmerged. Existing checks are pre-Tokyo evidence and are not
claimed as Tokyo tests. No existing branch, PR, evidence, media or protection was changed.

## Rules checked
- https://ethglobal.com/events/tokyo2026/info/start
- https://ethglobal.com/events/tokyo2026/info/details (read in real browser)
- https://ethglobal.com/events/tokyo2026/prizes/uniswap-foundation

Deadline: September 27, 2026, 09:00 JST (00:00 UTC). Internal handoff target: 08:00 JST.
Exact hacking start: September 25, 2026, 21:00 JST, verified in the official event schedule. Classic excludes pre-existing project-specific
code, designs and assets. A new repository/date does not establish eligibility.
Detailed rules require meaningful human contribution and disclosure of AI-assisted files and prompts.
They require 2–4 minute video, at least 720p, and prohibit synthetic/AI voiceover.

## Superseded Classic question — retained as history, not sent
I previously developed an Entrotter concept and separate Colosseum implementation before Tokyo.
For Tokyo I selected Start from Scratch and authored an independent, narrower Uniswap decision-checking
prototype during the event, without importing prior code, designs or assets. AI authored much of the
implementation under my specifications. Does the prior concept/product affect Classic eligibility,
and what evidence of my own substantive contribution do you require? I will not change tracks without
explicit approval and will disclose both prior work and AI assistance.

## Current Continuity disclosure
The prior Entrotter concept/product is disclosed above. This Tokyo prototype adds a newly authored, four-action Uniswap comparison with explicit user spending/gas constraints, a dedicated UI and new execution evidence. No old result or media is claimed as new work. The owner authorized Continuity after initial implementation began. AI-use and meaningful human contribution requirements still apply.

## Owner-directed migration into existing repositories
After authorizing Continuity, the owner explicitly required updating existing repositories and deleting the temporary `entrotter/tokyo2026` repository and local folder. The new code is retained in `engine/tokyo/`, UI in `entrotter.github.io/tokyo2026/`, and documentation/evidence in this existing coordination repository. New branches start from existing protected main; PR #47 and all related candidates are untouched. The temporary repository is not a submission source. Its in-session commits are recorded as provenance only, not pre-event work. No history is rewritten.
