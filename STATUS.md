# Verified implementation status

Recorded 2026-09-19. **Experimental local implementation, not a competition-ready
release, not a deployed service.** All repository names below are intended destinations.

## Implemented and exercised

- Six separate MIT-licensed repository directories with contribution/security guides,
  PR/issue templates and GitHub Actions configuration.
- Deterministic synthetic stress tests with causal hold/circuit-breaker policies,
  explicit fees and slippage, traces, drawdown and sealed JSON result artifacts.
- Three synthetic scenarios including an unfavorable recovery case; the generated
  public reports reproduce exactly. None is claimed to be historical evidence.
- Loopback-only development HTTP API; SDK and CLI round trips; artifact tampering
  rejection and input/transport boundaries.
- Genuine editable package installation and installed `entrotter` console-command
  smoke test passed. Runtime packages use only the Python standard library.
- Static, dependency-free documentation/report site with local JSON import,
  SHA-256 checking and no upload/account/wallet/payment functionality.
- Repo/Pages publication script, default dry-run, and a detailed Codex goal.

## Verification evidence

| Check | Observed outcome | Evidence |
| --- | --- | --- |
| Python unit and workspace integration tests | 105 passed, 1 skipped | `evidence/*-tests.log`, `evidence/verification.json` |
| Production website JavaScript functions tested in Node | 8 passed | `evidence/website-javascript-tests.log` |
| Editable installation and CLI run/verify/inspect | Passed | `evidence/package-install.log`, `evidence/package-smoke.log` |
| CLI -> SDK -> local HTTP API -> engine | Passed | `tests/test_workspace.py`, test logs |
| Three public example artifacts | Reproduced exactly, digest verified | Workspace tests and website report files |
| Actual Anvil execution | NOT RUN: executable unavailable | Explicit skipped integration test |
| Historical archive-state execution | NOT RUN: no archive RPC credential | No historical success claim |
| Full browser/visual/accessibility verification | BLOCKED before navigation | `evidence/browser-verification.json` |
| GitHub repository creation/push | NOT PERFORMED | GitHub tools read-only; no authenticated gh CLI |
| GitHub Pages deployment | NOT PERFORMED | Workflow prepared only, no public URL verified |
| Codex persistent goal | NOT REGISTERED | Goal files prepared; no active Codex session |

Do not equate 113 passing offline/HTTP/JavaScript tests with a verified historical
simulation. Mocks and synthetic examples are not live-chain or product-demand evidence.
The browser was blocked by an administrator navigation policy; no bypass was attempted.
The Python HTTP tests are not browser rendering tests.

## Implemented but not yet validated end to end

`engine/evm.py` owns two localhost Anvil instances and supports supplied local
transactions or an archive-state fork with pinned source metadata. Tests exercise
validation, transport restrictions and mocked lifecycle paths, but **the real Anvil
integration has not run in this environment**. It can contain bugs until that gate passes.
It re-executes supplied actions, not a changed market history or a complete alternative
future. Actor funding overrides and absent token valuation are disclosed in reports.

## Still to implement

- A useful ERC-20/DeFi action adapter and meaningful token/portfolio state deltas.
- A genuine historical scenario with verified source chain/block/hash and evidence.
- External agent integration, recorded tool actions, held-out benchmark scenarios.
- EVM report presentation in the website (currently only fixture results render).
- Production sandbox/resource quotas and hosted service hardening. The current API
  must remain localhost-only; no untrusted code execution is supported.
- Full browser/mobile/accessibility review; stronger release security and lint/type gates.
- Real user evaluations, recorded demo/pitch and owner-reviewed competition submission.

## Resume in an authorized Codex environment

Open the parent workspace containing all six directories. Read the root `AGENTS.md`,
`entrotter/CODEX_GOAL.md` and `entrotter/CODEX_START.txt`. Paste the latter into Codex to
set the current chat's persistent goal; files alone do not start or schedule Codex.

```bash
python3 entrotter/scripts/verify.py
python3 entrotter/scripts/publish.py          # review dry-run plan
# Requires gh authentication and permission in the existing entrotter organization:
python3 entrotter/scripts/publish.py --apply
# After installing the verified Foundry version in a suitable environment:
python3 entrotter/scripts/verify.py --require-anvil
```

If a repository now exists, inspect/clone it and reconcile through PRs. Never overwrite
remote work with this archive. The intended site is `https://entrotter.github.io/`,
**not a claim of a live deployment**. Do not create a CNAME or configure any custom domain.
Record actual URLs, SHAs, Actions outcomes and HTTP verification before updating status.

Progress toward the Colosseum quality target is governed by `CODEX_GOAL.md` and
`release-gates.json`. No winning outcome, uninterrupted execution or submitted entry
is claimed or guaranteed. At a blocker, checkpoint exact facts and continue independent
approved work rather than fabricating completion.
