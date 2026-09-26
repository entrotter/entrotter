# Verified implementation status

Updated 2026-09-20 JST. **Goal active; not submission-ready.** This turn made
implementation and deployment progress. All six repositories now exist publicly
under https://github.com/entrotter. Do not repeat archive bootstrap or overwrite
remote history. Use the existing six sibling Git checkouts and focused PRs.

## Verified progress

- Foundry v1.8.3 release archive downloaded and SHA-256 checked against GitHub
  release metadata. Local executable: `../.tools/foundry-v1.8.3/anvil` from this
  coordination repo. `evidence/foundry-install.json` records exact version/digest.
- Full workspace check: **121 Python tests and 13 JavaScript tests passed**,
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

## Open gates and next actions

1. All current engine/scenario/viewer changes are merged and live. Five component
   repos now require passing CI and one PR approval, including admins. Apply the
   same protection to coordination after its evidence checkpoint merges.
2. Complete security/delivery: whole-process CPU/RSS/time/disk/concurrency bounds,
   SIGTERM handling, deeper RPC/API fault tests, lint/types/security/dependency and
   docs-link CI, remaining immutable dependencies, and branch protections.
3. Add constrained causal agent observations/actions and one real recorded agent;
   disclose model/prompt/limits/cost. Build three sourced cases and untouched
   holdouts. Current manually prescribed actions are not an integrated agent.
4. Compare the same task with direct Anvil scripting. Historical trace replay remains unsupported; never
   describe archived-state actions as a reconstructed counterfactual market.
5. Complete accessibility/link review and submission materials. Actual pitch/demo
   videos, three genuine target-user evaluations, joined-event verification and
   owner eligibility remain pending. Outreach and submission require owner approval.

No arbitrary user code execution, public engine, paid service, package publication,
mainnet transaction, customer outreach or competition submission was performed.
The current per-EVM memory bound is not a complete process sandbox. Preserve these
limits in the product and release-gates.json. Overall completion remains unproven.


## ETHGlobal Tokyo Continuity preparation — September 26–27

Owner directed Tokyo work into the existing repositories and requested removal of the temporary separate repository. Runtime changes are scoped to engine `tokyo/`; UI to website `tokyo2026/`; submission documents and evidence are in `submission/tokyo2026/` and `evidence/tokyo2026/`. These changes use separate review branches based on main and do not merge or alter Colosseum PR #47 or its related candidates. See the Tokyo checklist for current tests, deployment limits and owner actions; earlier test results above remain historical. Independent approval is still required for protected-main integration.

### Tokyo Continuity migration verification

- Existing engine PR #25 (`42204e0c8091143e08f9f6525cbfebde741fb74a`) and website PR #13 (`6623671193dbaf5990078c1d2292e97730fc0c4c`) are public. Coordination PR #49 contains the submission packet. Existing Colosseum PR #47 and related branches remain preserved.
- Migration verification: 5 real archive/lifecycle checks passed, 80 existing engine tests passed, 10 Python and 13 Node existing website tests passed. Evidence: `evidence/tokyo2026/migrated-integration.json` and `existing-*-tests.log`. New 8 Python + 16 JS tests passed.
- Current engine CI matrix/EVM, website check and coordination integration passed. Website deployment is not performed on PRs and awaits independent main approval.
- Newly recorded 149-second silent captioned video published in the existing coordination repo: https://github.com/entrotter/entrotter/releases/tag/tokyo-continuity-demo . Supplemental partner-prize demo; not a compliant spoken Finalist video.
- Local temporary `tokyo2026` folder deleted after migration. Remote deletion failed because CLI token lacks `delete_repo`; do not claim remote deletion or use that repository as submission source.
- ETHGlobal final submission and Uniswap form completion remain unverified. Prepared files and clicked send buttons are not proof of acceptance.

### Tokyo submission form handoff
Uniswap required feedback displayed its thank-you confirmation. ETHGlobal details, three existing repos, images, AI disclosure, Continuity and Uniswap partner-only selection are saved. The optional official video field is skipped; the published silent recording remains a supplemental demo link. The final form still demands a no-pre-event-work declaration; automatic approval review rejected the final Submit action with it unchecked. Final submission has NOT occurred. See `evidence/tokyo2026/submission-progress.json`; owner/organizer clarification is required. No repository history or approvals were bypassed.

### Tokyo submission completed — September 27, 2026, 01:13 JST

After the owner explicitly confirmed the explained final declaration and instructed submission, the normal ETHGlobal final checkbox and Submit action succeeded. The live page displayed **You did it!**, **Thanks for submitting your project**, and **Partner Judging only**. The public showcase loads at https://ethglobal.com/showcase/entrotter-tokyo-4b9vf .

The entry preserves Continuity, existing-repository source links, prior-work and AI disclosures, and the supplemental silent recording link. The official optional video field is skipped. Required Uniswap feedback is confirmed submitted. Eligibility/prize acceptance remains subject to organizers; no prize or stake-return claim is made. The earlier blocked state above is historical and superseded by this confirmed submission.

Remaining repository operations: website PR deployment awaits independent approval; remote temporary repository deletion remains blocked by CLI delete_repo scope. Local temporary folder is deleted. Source code and all former PRs/history remain preserved.
