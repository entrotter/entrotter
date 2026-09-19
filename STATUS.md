# Verified implementation status

Updated 2026-09-20 JST. **Goal active; not submission-ready.** This turn made
implementation and deployment progress. All six repositories now exist publicly
under https://github.com/entrotter. Do not repeat archive bootstrap or overwrite
remote history. Use the existing six sibling Git checkouts and focused PRs.

## Verified progress

- Foundry v1.8.3 release archive downloaded and SHA-256 checked against GitHub
  release metadata. Local executable: `../.tools/foundry-v1.8.3/anvil` from this
  coordination repo. `evidence/foundry-install.json` records exact version/digest.
- Full workspace check: **145 Python tests and 13 JavaScript tests passed**,
  including actual Anvil transfer/revert/rejection, state isolation, startup
  timeout/cancellation, missing receipt cleanup, token storage and decimal pins.
  Fault-injection tests are labelled; no real EVM test was silently replaced.
- Engine PRs #6 and #7 merged after passing Python matrix and dedicated real EVM
  CI. Current engine: `6a3e03341eccd44fcd04a990db21cc5509e0c84d`.
- Exact ERC-20 token deltas and legacy Uniswap v3 ABI builder implemented.
  Scenario PR #4 merged. Website PR #7 merged; follow-up improves summary units.
- Actual Ethereum block 19,000,000, hash
  `0xcf384012b91b081230cdf17a3f7dd370d8e67056058af6b272b3d54aa2714fac`:
  baseline swaps 1 WETH into 2,556.134769 USDC. Candidate's excessive minimum
  output reverts, retains 1 WETH and consumes gas. Initial tracked balances and
  native funding are identical. No portfolio valuation or profit is asserted.
- Two historical runs produced identical complete artifacts, measured at 9.365
  and 8.621 seconds. `evidence/historical-verification.json` records CPU and peak
  child RSS with measurement scope. `historical-uniswap.json` contains receipts.
- Offline example reproduced from fresh public dependency checkouts and a new
  venv without pip/system packages in 5.335 seconds. Exact pins and scope are in
  `evidence/clean-reproduction.json`; the coordination checkout was already present.
- The historical example also reproduced from clean public checkouts in a fresh
  venv in 13.877 seconds, matching the public artifact exactly. See
  `evidence/clean-historical-reproduction.json`.
- Initial Pages deployment succeeded and live HTML matched the repository.
  Browser checks covered desktop/mobile, negative fixture, hash rejection,
  hostile Unicode/HTML-like input, no upload/third-party requests and skip link.
  Latest EVM viewer is also verified live: deployment run 35453228118, commit
  `ab121348b0ffbec5650f9eadf0a0b11f639d9780`. See `evidence/browser-verification.json`.
- Private vulnerability reporting enabled and independently read back on all six
  repositories. `evidence/repository-security.json` records results.
- Official Colosseum event/rules checked: deadline October 12, 2026 at 23:59 PT
  = October 13 at 06:59 UTC / 15:59 JST. `docs/COMPETITION.md` links sources.

## Reproduction commands

From the parent workspace (not this repository):

```bash
PATH="$PWD/.tools/foundry-v1.8.3:$PATH" python3 entrotter/scripts/verify.py --require-anvil
python3 entrotter/scripts/reproduce_clean.py
# Add --historical with the archive/Foundry environment below for a clean fork run.
SSL_CERT_FILE=/etc/ssl/cert.pem PATH="$PWD/.tools/foundry-v1.8.3:$PATH" PYTHONPATH=engine/src ENTROTTER_RPC_URL=https://eth.drpc.org python3 entrotter/scripts/check_historical.py
```

The TLS bundle override is for this macOS Python installation; do not disable
certificate validation. Public archive service availability can change. PublicNode
served the 2024 block header but rejected state reads as pruned. dRPC served the
required historical state. Archive failure is explicit, never a synthetic fallback.

## New agent slice: verified locally, awaiting independent review

- Engine PR #8 (`bb8b3e8d32c7cbd49629d337758f30bfdf805045`) adds typed
  execute/hold decisions over current observations, a bounded gas budget and exact
  recorded replay. Its Python matrix and dedicated real-Anvil CI passed.
- Scenarios PR #5 (`828cfe37f2a2d6d7f2db868a0856a28c080b7a94`) defines the
  optional result recording schema; its validation CI passed. Both PRs are open,
  not merged. Main still requires an independent approval.
- A real `gpt-5.6-sol` Codex CLI policy completed two decisions on an artificial
  local-EVM transfer/revert example. Non-agent execution reverted once (42,006 gas);
  both deterministic risk and model policies executed the transfer and held the
  revert (21,000 gas). The model took 8.721 seconds versus risk 0.313 seconds; no
  model advantage is demonstrated. Model alias, exact prompt, usage, limits and
  unavailable seed/monetary cost are recorded, not invented.
- Complete model artifact `1d1de88d01cbe23c494f6a6f7ee7127d63629baac071def58c067506ddf5893b`
  reproduced exactly without a model call. Fresh public dependency checkouts and
  a stdlib-only venv reproduced it in **5.148 seconds**, including clone/setup.
  See `evidence/clean-agent-reproduction.json` and `docs/AGENT_EVALUATION.md`.
- Trusted CLI subprocess timeout/output/error handling and cleanup pass offline
  tests. This is not a general code sandbox or an egress firewall. No arbitrary
  providers can be selected through JSON/HTTP. Current dependency pins identify
  tested proposed engine/schema commits, pending independent review.

## Frozen historical agent evaluation completed

- Three sourced Ethereum/Uniswap states plus two implementation holdouts were
  evaluated with identical proposals and starting states. Scenario freeze commit
  `1ce15d9` predates new protocol-state execution; 19M remains explicitly explored.
  Scenarios PR #6 (`5b718984ac67b8fb49e02f4dab676ae212d2aa58`) has passing CI.
- At 17M and 20M all policies executed successful swaps. At 18M, 19M and 21M,
  prescribed swaps reverted while both risk/model policies held. Model and risk
  observations, choices, final metrics and token balances agree in every case.
  The model was slower in all five; no model superiority or portfolio PnL claimed.
- All ten risk/model reports replayed exactly from recordings on fresh forks.
  All 15 report hashes, ten agent schemas, and receipt-derived gas arithmetic
  passed post-run inspection. Evidence: `evidence/causal-v1/`, with the initial
  missing-RPC failure retained. See `docs/HISTORICAL_AGENT_EVALUATION.md`.
- Engine/agent schema/model integration remain pending independent review in
  engine #8, scenarios #5/#6 and coordination #8/#9.
  Coordination #8 integration CI passed. The holdouts are now evaluated; do not
  reuse them as untouched cases for a tuned policy. All source/prompt pins remain.

## Open gates and next actions

1. The earlier EVM/viewer changes are merged and live; new agent PRs above are open. All
   six repositories now require passing CI and one PR approval, including admins.
   Protection read-back is in evidence/branch-protection.json. Future PRs need a
   reviewer distinct from the author; do not bypass these protections. The final
   protection checkpoint is committed locally pending the next reviewed docs PR.
2. Complete security/delivery: whole-process CPU/RSS/time/disk/concurrency bounds,
   SIGTERM handling, deeper RPC/API fault tests, lint/types/security/dependency and
   docs-link CI, remaining immutable dependencies, and branch protections.
3. Obtain independent review of the agent and benchmark PRs. Further policy
   tuning needs new unused cases; these two holdouts are now evaluated. The original
   archived Uniswap report remains a manually prescribed intervention example.
4. Next implementation slice: compare the frozen 19M task with a standalone
   direct Anvil script, preserving identical proposals, source pins and outcome
   checks. Record runtime without claiming a statistical speed advantage. Historical trace replay remains unsupported; never
   describe archived-state actions as a reconstructed counterfactual market.
5. Complete accessibility/link review and submission materials. Actual pitch/demo
   videos, three genuine target-user evaluations, joined-event verification and
   owner eligibility remain pending. Outreach and submission require owner approval.

No arbitrary user code execution, public engine, paid service, package publication,
mainnet transaction, customer outreach or competition submission was performed.
The current per-EVM memory bound is not a complete process sandbox. Preserve these
limits in the product and release-gates.json. Overall completion remains unproven.
