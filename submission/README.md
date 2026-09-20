# Entrotter submission index

**Review package, not a submitted entry.** Recorded videos accompany the code and
measured evidence. Owner fact-checking, team/registration verification, independent
code approval and genuine user validation remain open. No entry or outreach has
been sent. Re-check the live submission form before uploading anything.

## Product

**Entrotter — a local test bench for onchain agent decisions.** Start from a known
blockchain state, change one decision, and retain an experiment another developer
can inspect and reproduce. The initial audience hypothesis is small EVM agent
teams already maintaining their own simulation scripts.

The engine runs paired local Anvil branches or forks pinned historical state.
Versioned reports record assumptions, source pins, overrides, receipts, native and
ERC-20 units, constrained agent observations/actions and replay records. A static
viewer imports reports locally in the browser. No signing key or mainnet write is
required. Archived-state action execution is not historical transaction replay,
a prediction of future markets, or a measurement of profit.

## Submission materials

| Material | Artifact | Status |
| --- | --- | --- |
| Product demo | [MP4](media/entrotter-demo.mp4), [VTT](media/entrotter-demo.vtt), [SRT](media/entrotter-demo.srt) · 2:54.24 | Recorded actual Chromium interactions and bounded engine calls; review cut |
| Product pitch | [MP4](media/entrotter-pitch.mp4), [VTT](media/entrotter-pitch.vtt), [SRT](media/entrotter-pitch.srt) · 2:51.44 | Recorded presentation with synthetic narration; owner/team context still required |
| Video production evidence | [Manifest](../evidence/submission-media/manifest.json) | Source pins, exact scripts/timelines, output hashes, execution and rendering checks |
| Pitch text and shot list | [Video scripts](VIDEO_SCRIPTS.md) | Exact narration, including hypotheses and limitations |
| Market/pricing/distribution | [Market hypotheses](MARKET.md) | Unvalidated, no fabricated TAM/customer/revenue claim |
| Target-user evaluation | [Evaluation protocol](EVALUATIONS.md) | Three genuine sessions required; zero completed records |
| Development/AI disclosure | [Disclosure](DISCLOSURE.md) | Supplied archive and substantial Codex assistance disclosed; owner dates/rights need confirmation |
| Rules, deadline and eligibility | [Competition requirements](../docs/COMPETITION.md) | Public requirements rechecked; joined-account state and owner eligibility unverified |

Both videos explicitly label synthetic narration and pending owner review. The
demo uses actual product UI, a clearly labelled recording console displaying real
process output, and generated report files. It does not stage successful output,
claim to be the founder speaking, or present the recording console as a product
feature. The pitch is an artifact for owner review; it does not establish founder
communication or market fit. No video platform has received an upload.

## Exact review sources

| Component | Source | Review state |
| --- | --- | --- |
| Bounded causal-agent engine | [engine abb4662](https://github.com/entrotter/engine/tree/abb4662ce960e08b2aa3a2c8a1c10719339edccc) | [PR #21](https://github.com/entrotter/engine/pull/21), stacked prerequisites pending independent review |
| Viewer used in recording | [website 6174031](https://github.com/entrotter/entrotter.github.io/tree/61740312f281f7e911e0eb6e9482a3c372cb1fae) | [PR #11](https://github.com/entrotter/entrotter.github.io/pull/11), not deployed |
| Frozen evaluation implementation | [engine bb8b3e8](https://github.com/entrotter/engine/tree/bb8b3e8d32c7cbd49629d337758f30bfdf805045) | Original benchmark/source boundary retained |
| Frozen scenarios | [scenarios 5b71898](https://github.com/entrotter/scenarios/tree/5b718984ac67b8fb49e02f4dab676ae212d2aa58) | Original cases and evaluated holdouts unchanged |
| Reproduction evidence | [coordination 67b7d19](https://github.com/entrotter/entrotter/tree/67b7d19105495e314c308cd7e2e01ef254f37ca1) | [PR #39](https://github.com/entrotter/entrotter/pull/39), independent review pending |
| Public site | [entrotter.github.io](https://entrotter.github.io/) | Live earlier viewer; do not confuse with the recorded review branch |

Six public repositories: [coordination](https://github.com/entrotter/entrotter),
[engine](https://github.com/entrotter/engine), [SDK](https://github.com/entrotter/sdk-python),
[CLI](https://github.com/entrotter/cli), [scenarios](https://github.com/entrotter/scenarios),
and [viewer](https://github.com/entrotter/entrotter.github.io). Original project
code is MIT licensed. Packages and worker images are not published to registries.

## Evidence and differentiation

[Bounded reproduction](../docs/BOUNDED_AGENT_REPLAY.md) matched all 19 original
complete EVM reports, including 12 agent recordings, with no new agent-model call.
The new demo performs an additional real local risk run and frozen-model replay.
This proves a reproducible observation/action contract, not a better model.
[Historical evaluation](../docs/HISTORICAL_AGENT_EVALUATION.md) includes three
sourced cases plus two pre-frozen holdouts; those holdouts are now consumed. The
model matched the risk rule and was slower in every evaluated case.

[Direct Anvil comparison](../docs/DIRECT_ANVIL_COMPARISON.md) produced identical
common outcomes in six runs, with medians of 8.653 seconds for the bespoke script
and 8.689 for Entrotter. No speed or developer-productivity advantage is proven.
The proposed difference is reusable scenario validation, recorded causal decisions,
exact replay and a shareable report/inspection workflow. A few Anvil scripts may
be the right solution for a single bespoke experiment. Actual willingness to adopt
or pay for the broader workflow is still a hypothesis.

## Owner facts needed before submission

| Required fact | Current state |
| --- | --- |
| Team members, locations, backgrounds and founder motivation | Not supplied/confirmed; do not infer from the filesystem or GitHub profile |
| Every member registered for the joined event; leader/team mapping | Not verified in an authenticated account |
| Age/location/employment/rights eligibility | Owner must confirm against official rules |
| Funding history and all relevant prior development | Unverified; archive provenance is disclosed separately |
| Genuine evaluation records and permission to quote | No completed sessions or quotes |
| Final video approval, founder introduction and submission consent | Pending |
| Protected integration, site deployment and exact submitted code pins | Pending independent review; never bypass protections |

The material is not a claim of a win, market validation or complete goal acceptance.
