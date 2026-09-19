# Verified implementation status

Updated 2026-09-20 JST. **Goal active; not submission-ready.** This turn made
implementation and deployment progress. All six repositories now exist publicly
under https://github.com/entrotter. Do not repeat archive bootstrap or overwrite
remote history. Use the existing six sibling Git checkouts and focused PRs.

## Verified progress

- Foundry v1.8.3 release archive downloaded and SHA-256 checked against GitHub
  release metadata. Local executable: `../.tools/foundry-v1.8.3/anvil` from this
  coordination repo. `evidence/foundry-install.json` records exact version/digest.
- Full workspace check: **150 Python tests and 13 JavaScript tests passed**,
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

## Direct Anvil comparison and diagnostic hardening

- The independent stdlib/JSON-RPC script and Entrotter executed the same frozen
  19M paired task three times each, in alternating order. All six outcomes match
  the source pin, every complete receipt, per-step native/token balances and gas.
  Observed median wall times: direct 8.653 seconds, Entrotter 8.689 seconds. This
  small network-dependent sample does not show a speed advantage. See
  `docs/DIRECT_ANVIL_COMPARISON.md` and `evidence/direct-anvil-comparison.json`.
- Entrotter additionally supplies reusable scenario validation, typed decision
  records/replay and a shareable report workflow. Contributor productivity and
  demand are not established by these measurements; genuine evaluations remain.
- Engine PR #9 (`ca9d5a7`) removes all provider error fields from user-facing RPC
  rejection diagnostics. Its regression tests failed before the patch and the
  isolated main-based checkout passed 83 tests with real Anvil afterward. See
  `evidence/engine-rpc-diagnostics-tests.log`. The primary engine checkout remains
  at the frozen benchmark commit; the fix awaits independent review and merge.
- Workspace tests pass 150 Python and 13 JavaScript tests without skips. The
  separate 83-test hardening run overlaps the suite and is not added to that total.

## Native lifecycle and optional bounded workers

- Engine PR #10 (`7f08a2b`) adds a lifetime-pipe guardian for owned Anvil nodes.
  Real owner SIGTERM/SIGKILL, guardian loss and watchdog checks passed in the
  88-test main-based suite; Python-matrix and real-EVM CI passed. Node lifetime
  is 150 seconds plus termination grace, not a native CPU/RSS sandbox.
- Engine PR #11 (`05448c3335440f19e619d1b71b449f4f0fb470d6`) adds explicit
  `run --isolated` / `serve --isolated` with a locally built immutable Docker
  image and verified Linux cgroup v2 controllers. Per-run limits: one CPU quota,
  512 MiB/no swap, 128 PIDs, read-only non-root rootfs, 64 MiB tmpfs and 16 MiB
  shared memory, 256 KiB input, 8 MiB output, and a 180-second worker timer.
- The main-based worker checkout passed 96 unit/native-Anvil tests. Actual Docker
  checks exercise kernel CPU throttling, OOM kills, fork exhaustion, full tmpfs,
  noexec, CLI/API report equality and signal/owner-loss cleanup. Dedicated local
  and Linux CI both passed all 10 tests, including an unattended 180.916-second
  local expiry. Linux run: 35458208203. See `evidence/worker-security.json`.
  No owned containers remained afterward; the dedicated VM is stopped and the
  existing Docker context/default profile is unchanged.
- The isolated historical 19M Uniswap run matched the complete existing public
  artifact exactly in 10.055 seconds. No archive URL or credentials are included
  in reports. Image inputs/source hashes are in `evidence/isolated-worker-image.json`.
- Native mode remains the default. Fork workers use bridge networking, not an
  archive-host egress firewall. Arbitrary agent code remains disabled. At that checkpoint, host report/image/VM storage,
  aggregate CLI concurrency and API connection threads still needed bounds.
  The newer host-budget slice below addresses API storage and connections. PRs #9/#10/#11 await independent review and are not merged.
  These test counts overlap previous engine suites; do not add them to the
  frozen workspace's 150 Python/13 JavaScript count.

## Host report storage and API connection bounds

- Engine PR #12 (`5e2663661cb26b17247ed34b2f31297095ba65e6`) bounds the
  dedicated API report directory to 128 MiB/128 files, individual reports to 8 MiB,
  and connections to eight handlers with a 240-second absolute socket deadline.
  Real file/process/socket tests cover capacity exhaustion, simultaneous writers,
  trickled headers, timeout recovery, wrong stored IDs and atomic write failure.
- Standalone CLI PR #5 (`d842c56bd9cf2c0845f5666b4ea0b02d2be34489`) enforces
  the same 8 MiB export limit and preserves prior destinations on failure without
  adding an engine dependency. Oversize/content-ID regressions failed before fixes.
- Engine 114 native/unit tests and CLI nine tests passed locally. Engine Python
  matrix, real-Anvil and actual-Docker CI, plus CLI Python matrix, all passed.
  A real CLI→SDK→API check verified fixture/Anvil reports, 507/503, no POST retry,
  saved/exported equality and recovery. `scripts/check_host_limits.py` makes it
  reproducible; its dedicated pinned CI job and existing workspace job both
  passed (run 35459506934). Linux and macOS artifact IDs agree. Frozen benchmark
  inputs are unchanged. See `evidence/host-resource-bounds.json`.
- These are application file-content limits, not whole-filesystem/VM quotas.
  Independent CLI export retention/concurrency, image/VM storage, native-default
  execution and complete CI hygiene remain open. Socket timeout does not forcibly
  cancel admitted native Python work. PRs remain unmerged pending independent review.

## Engine quality and Python dependency gates

- Engine PR #13 (`ba0adfb233b685f99f35cbbe33331fee83360504`) adds Ruff lint/
  formatting and mypy over all 17 production source/scripts, fixing 28 initial
  lint and 19 initial typing findings. JSON boundaries still need runtime validation.
- Full Bandit scanning retains 15 expected findings (13 low, two medium), with
  exact code/source hashes and per-finding reasons. No rules or advisory IDs are
  suppressed. Author-reviewed reasons still need independent approval; this is
  not a proof of security. Policy failure paths are tested.
- All 42 Python tool/build dependencies are version/hash locked; the strict audit
  reported no known vulnerabilities and no skipped packages. Runtime dependencies
  remain empty. All engine GitHub Actions now use immutable commit IDs.
- The local suite passed 121 tests with real Anvil. The full historical Uniswap
  artifact still matches exactly. An MIT-licensed wheel with no runtime dependencies
  built and reproduced the fixture from a fresh venv in isolated Python mode.
  See `docs/ENGINE_QUALITY.md` and `evidence/engine-quality.json` for exact scope.
- Linux quality checks passed. The first job omitted hidden generated report files
  from its upload; this was fixed with explicit hidden-file inclusion and an error
  on missing output. Final quality/native/Docker/matrix CI all passed; downloaded
  reports retain all 15 findings and the 42-package audit. The CI wheel's 14 Python
  files match the tested source. Other repos, native/container-OS audits and
  docs-link gates remain open.

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
4. The same-task direct Anvil comparison is now measured. Continue the remaining
   security/delivery gates next: default bounded execution, aggregate CLI budgets
   and CI lint/types/dependency/security/docs-link checks. Preserve the frozen engine checkout; use an isolated worktree.
   A dedicated local Colima profile now provides a verified Linux cgroup v2
   Docker daemon. The opt-in worker is tested in engine PR #11; native execution
   remains the default. See docs/WORKER_SECURITY.md and its measured evidence.
   Historical trace replay remains unsupported; do not imply a reconstructed market.
5. Complete accessibility/link review and submission materials. Actual pitch/demo
   videos, three genuine target-user evaluations, joined-event verification and
   owner eligibility remain pending. Outreach and submission require owner approval.

No arbitrary user code execution, public engine, paid service, package publication,
mainnet transaction, customer outreach or competition submission was performed.
The current per-EVM memory bound is not a complete process sandbox. Preserve these
limits in the product and release-gates.json. Overall completion remains unproven.
