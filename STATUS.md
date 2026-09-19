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
  files match the tested source. At that checkpoint, other repos, native/container-OS audits and
  docs-link gates remained open; subsequent slices are recorded below.

## Documentation links verified across all six repositories

- Checksum-pinned Lychee 0.24.2 checks each PR's tracked Markdown/HTML/CSS,
  including hidden templates, local files, fragments and public HTTP links.
  Six real-checker regression tests prove missing targets/fragments/CSS/HTTP 404
  failures, tracked-input coverage and rejection of an empty successful scan.
- All six local scans and all six GitHub link jobs passed: 102 successful link
  occurrences, one explicitly excluded local API example, no errors/timeouts.
  Downloaded CI reports match every local input hash; CI records its merge SHA.
  Complete results are in evidence/docs-links/summary.json and adjacent reports.
- README navigation now links workspace setup, contributing, security and license.
  Previously engine/SDK had zero extracted links and CLI only an excluded example.
  Consumer actions use immutable coordination commit ea74aec66c5234edb935e4b12c14ec686dc73f80.
  PRs: coordination #16, engine #14, SDK #5, CLI #6, scenarios #7, website #9.
  These are unmerged, pending independent review. Main required-check lists are
  unchanged. Static scanning does not complete the accessibility/dynamic UI gate.
- An existing host-bounds job failed at its CLI 503 assertion (run 35461539934).
  A local saturated-API probe reproduced five generic transport errors in 59 CLI
  attempts while all eight slots stayed occupied. It is not a link-check failure.
  The failure log/probe are retained; the subsequent fix and regression are
  recorded below. Frozen engine
  and historical scenario inputs remain unchanged.

## Saturated API response race: fix under review

- The earlier 503 failure is reproduced by a real socket that sends a POST body
  after the server has already emitted its response. Immediate close caused
  BrokenPipe; the new regression fails before the fix and passes afterward.
- Engine PR #15 adds bounded draining after half-closing the 503 output: at most
  320 KiB and 100 ms including send, without a new handler or admitted experiment.
  Idle/trickling rejected clients cannot extend the absolute grace. Slow or
  oversized senders can still see transport failure when the grace expires.
- All 124 native/unit tests passed locally. Ruff lint/format, mypy and full Bandit
  checks pass; all 15 finding fingerprints are unchanged. Only the reviewed API
  source hash changes. An existing deadline-abort test now correctly accepts FIN
  or reset while preserving timeout/recovery assertions; its failure is retained.
- The actual CLI→SDK→API check now requires 16 consecutive busy CLI responses and
  verifies no work, no replacement export, 507 handling, real Anvil reports and
  recovery. Local and Linux verification passed; full artifact IDs and checker hashes agree.
  The exact engine fix commit passed Python matrix, 124 native tests, all ten real
  Docker enforcement tests, quality and link jobs. Downloaded quality evidence
  retains 15 findings, audits 42 packages without known vulnerabilities, and the
  wheel's 14 Python files match source. Coordination integration/link CI passed.
  See evidence/overload-response/summary.json. PRs engine #15 and coordination #17
  remain unmerged pending review. This does not erase the original failed run or
  complete broader gates. Live Pages again returned 200 with exact source HTML.

## SDK and CLI quality gates

- SDK PR #6 and CLI PR #7 add Ruff lint/format, normal mypy, complete unsuppressed
  Bandit scans, strict advisory audits of all 42 locked tool/build packages, and
  fresh-wheel checks. SDK has no runtime dependencies. CLI builds its unpublished
  SDK dependency from exact source b0c2ba3bba411e548af44101ae06e879bd7b5dc0,
  verifies its dependency graph and never resolves it from a package registry.
- SDK 18 and CLI 13 local tests pass. The SDK now ships its verified `py.typed`
  marker. The CLI's optional engine stub describes only the v0.1 boundary; actual
  engine behavior is separately tested. Source scans cover four SDK/five CLI
  files, with zero findings/skips. Both 42-package audits report no known issues.
- A correctly hashed array/object mode previously raised TypeError. The SDK's
  failing regression is retained; it now emits ClientError, and CLI rejects the
  report without a traceback. All 16 existing archived-state/agent reports pass
  hash/parser checks. This does not constitute new historical/model execution.
- Fresh venv installs use only local wheels with `--no-index --no-deps`, confirm
  MIT metadata/source equality, and exercise SDK import and CLI doctor/verify/
  inspect without an engine package. Real CLI→SDK→API fixture/Anvil, quota and
  16-attempt overload/recovery checks pass locally. SDK and CLI quality/matrix/
  link CI passed. The newly pinned Linux cross-repository job also passed; exact
  source pins, checker hash and complete report IDs match local results. Downloaded
  SDK/CLI quality reports match every scanned source hash; both CI wheel contents
  and MIT/dependency metadata were checked. See docs/SDK_CLI_QUALITY.md and
  evidence/sdk-cli-quality/summary.json. Coordination PR #19 records the evidence;
  all three PRs remain unmerged and require independent review.

## Report viewer accessibility and browser CI

- Website PR #10 (`d7785e201a4de50b72623a1e7522762738abab54`) fixes skip-link
  focus, 339px page overflow at a 320px viewport, keyboard scrolling in report
  tables/JSON, accessible chart observation data and empty tables after errors.
  The earlier skip-link smoke check established scrolling, not focus transfer;
  this deeper regression records that distinction.
- The identical runner/Chromium 153 rejects the previous website (16 failed
  groups, two passed) and passes all 18 groups after changes on macOS and Linux.
  Fourteen axe scans per final run have zero violations. Incomplete contrast
  results remain explicit, with separate solid-CSS calculations; manual screen-
  reader certification and complete WCAG conformance are not claimed.
- Ten website Python and 13 JavaScript tests pass. Exact/integrity-locked browser
  development dependencies have no reported known npm advisories. They are excluded
  from deployment. Pages build depends on unit and browser jobs, and its actions
  are immutable. Linux run 35464241907 and links 35464241911 succeeded; downloaded
  source/runner hashes match local evidence. See docs/WEBSITE_ACCESSIBILITY.md and
  evidence/website-accessibility/summary.json for failures, screenshots and scope.
- Existing live HTML still matches main ab121348b0ffbec5650f9eadf0a0b11f639d9780
  with HTTP 200. Accessibility changes are unmerged and not deployed; independent
  review remains required. Owned browser/server and clean baseline worktree were
  removed. Frozen engine/scenario inputs are unchanged.

## Proposed bounded execution defaults

- Engine PR #16 (`dddba4a2c3efdd429e36520e8fc9d163888089e2`) routes public runner,
  CLI and API defaults through the existing bounded worker; missing configuration
  fails closed. Native execution requires an explicit developer opt-out. CLI PR
  #8 (`952bfb5aba14b674dd959035a5625fadbd2b07d1`) adds --local --native, rejects
  older unsupported engines and cannot override an API server's mode.
- Three default-path checks failed before the change and a FIFO input timed out.
  Inputs now require regular files and bounded reads. Afterward 129 unit/native
  engine tests, ten real Docker tests, 15 CLI tests and 20 coordination tests pass.
  Default runner/engine CLI/API and standalone CLI results agree; missing workers
  preserve exports. An independent idle worker expired after 181.405 seconds.
- Actual default CLI-SDK-API fixture/Anvil, 507, 16 busy responses and recovery
  pass. The default archived 19M run matches the complete prior artifact in
  10.097 seconds. A fresh public checkout, venv, image build and verified default
  fixture run took 11.682 seconds with an already-running daemon and warm caches.
  No cold-machine installation or new model/market-performance claim is made.
- Engine/CLI quality, matrix, native/Docker and link CI passed. Downloaded scans
  match source; engine retains 15 findings, CLI has none, and each 42-package audit
  reports no known vulnerabilities. Downloaded MIT wheels match source and pass
  a fresh installed default-run/failure-preservation check. Coordination
  PR #23's three integration jobs passed (35465814576), plus links 35465814613.
  Downloaded source/runner/artifact pins agree; Linux clean default reproduction
  took 7.444 seconds including Foundry download, with warm Docker build caches.
  The dedicated VM is stopped, no owned workers remain and Docker context is unchanged.
- See docs/BOUNDED_DEFAULT.md, bounded-worker-pins.json and
  evidence/bounded-default/summary.json. Both changes remain unmerged, the frozen
  engine/scenario checkouts are unchanged, and the separate agent branch is not
  incorporated. Aggregate CLI admission/retention and image/VM disk remain open.

## Proposed admission shared by independent CLI/API processes

- Engine PR #17 (`0718b20e47a2b69dcd6ac2ac7112f189131f9ec6`) reserves one
  worker container name per configured Docker daemon. Preflight rejection is API
  429; a simultaneous creation conflict can return 422 because Docker reserves
  names before they appear in queries. No automatic retry or native fallback is
  introduced. Cleanup filters a unique owner label and removes only the full ID.
- Both real CLI/API checks failed at parent dddba4a. The final source passes 135
  unit/native-Anvil tests and 15 actual Docker tests, including a synchronized
  two-process creation race, timeout/recovery and an unstarted occupied slot.
  The real idle worker expired after 181.203 seconds and subsequent runs worked.
  These suites overlap prior engine evidence; do not add them to frozen totals.
- Ruff/mypy, full Bandit review and docs links pass. Downloaded Linux quality
  reports retain all 15 findings, match the local full scan, and audit all 42
  Python packages without reported known vulnerabilities. All 14 Python files
  in the MIT wheel match source. Actual standalone CLI-SDK-API worker occupancy,
  one-POST 429 rejection, preserved exports/incumbent, 507/503 and recovery pass.
  All five engine Linux workflows, including 15 real Docker tests, passed at
  the exact source commit. Coordination PR #25 passed all three integration jobs
  (35467629251) and links (35467629252); downloaded pins, checker, image source
  and complete report IDs agree. Fresh public clone/venv/build reproduction took
  7.638 seconds on Linux with running Docker and warm build caches, not a cold
  machine install. No owned workers remain; the dedicated VM is stopped.
- See docs/DAEMON_WORKER_ADMISSION.md. Frozen benchmark checkouts remain unchanged.
  This limits cooperating default worker containers on one daemon, not caller
  processes, old/native clients, multiple daemons or image/export/VM storage.
  Containers abandoned before entrypoint start may require operator recovery;
  no daemon-failure guarantee or public multi-tenant safety is asserted.
  Independent review/merge remains required; the overall goal stays active.

## Worker image advisory and provenance gate in progress

- The prior actual worker scan reported 151 Debian package findings and six pip
  findings; a signed distroless alternative still reported 130 findings. Full
  inventories are retained. The selected digest-pinned public Chainguard Python
  3.14 base and built worker inventory 26 packages, including Python/libc/TLS,
  with no known reported findings at the recorded database timestamp.
- Engine commit `a9741942d9a4a87de62f9b9b90fb6cbe7d092648` adds checksum-pinned
  Cosign/Trivy, exact signing identity/image/source checks, database freshness,
  mandatory core-package coverage and failure on every finding. All severities
  and unfixed issues remain enabled. Native Anvil inventory is still outside
  coverage; the checksum-verified binary's individual digest is recorded.
- Local 142 unit/native-Anvil and 16 real Docker tests pass. The initial CPU
  probe failed under Python 3.14's changed multiprocessing default; it now uses
  explicit fork and asserts child exit codes plus actual throttling. The first
  failure is retained. Ruff/mypy/full 20-finding Bandit policy and 42-package
  Python advisory checks pass. Actual standalone CLI-SDK-API integration passes,
  and two 19M fork runs match the complete existing artifact (9.528/9.150 seconds).
  Linux matrix/native/quality/link CI passes; actual Linux image CI is pending.
- See docs/WORKER_IMAGE_AUDIT.md and evidence/worker-image-audit/. This does not
  close native dependency, host caller/disk, independent review or submission
  gates. Frozen engine/scenario checkouts remain unchanged.

## Open gates and next actions

1. The earlier EVM/viewer changes are merged and live; new agent PRs above are open. All
   six repositories now require passing CI and one PR approval, including admins.
   Protection read-back is in evidence/branch-protection.json. Future PRs need a
   reviewer distinct from the author; do not bypass these protections. The final
   protection checkpoint is committed locally pending the next reviewed docs PR.
2. Complete security/delivery: whole-process CPU/RSS/time/disk/concurrency bounds,
   SIGTERM handling, deeper RPC/API fault tests, lint/types/security/dependency and
   remaining repo quality CI, immutable dependencies, and branch protections.
3. Obtain independent review of the agent and benchmark PRs. Further policy
   tuning needs new unused cases; these two holdouts are now evaluated. The original
   archived Uniswap report remains a manually prescribed intervention example.
4. The same-task direct Anvil comparison is now measured. Continue the remaining
   security/delivery gates next: host caller/storage budgets, review/integration of the
   proposed bounded default and shared daemon admission,
   and remaining repo quality/native dependency checks. Preserve the frozen engine checkout; use an isolated worktree.
   A dedicated local Colima profile now provides a verified Linux cgroup v2
   Docker daemon. The opt-in worker is tested in engine PR #11; native execution
   remains the main-branch default until PR #16 is reviewed and merged. See docs/WORKER_SECURITY.md and its measured evidence.
   Historical trace replay remains unsupported; do not imply a reconstructed market.
5. Obtain independent review of the accessibility PR, deploy through protected main,
   and verify the live site; manual assistive-technology evaluation remains open.
   Continue submission materials. Actual pitch/demo
   videos, three genuine target-user evaluations, joined-event verification and
   owner eligibility remain pending. Outreach and submission require owner approval.

No arbitrary user code execution, public engine, paid service, package publication,
mainnet transaction, customer outreach or competition submission was performed.
The current per-EVM memory bound is not a complete process sandbox. Preserve these
limits in the product and release-gates.json. Overall completion remains unproven.
