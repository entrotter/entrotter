# Entrotter — ETHGlobal Tokyo 2026 execution brief for Codex

Prepared: 2026-09-26 JST

**Dispatch status:** This is a handoff document, not a running Codex task. The
GitHub connection allowed inspection but rejected both issue creation and a PR
comment with HTTP 403, `Resource not accessible by integration`. No issue or
comment was created, no Codex run was confirmed, and no submission was made.

## 1. Owner objective and execution boundaries

Inspect the existing Entrotter workspace and prepare a working, evidence-backed
ETHGlobal Tokyo 2026 submission candidate. Execute the necessary engineering,
tests, recording and documentation rather than returning only a plan.

The owner previously selected **Start from Scratch**. Preserve that selection
unless the owner explicitly authorizes a change. Preserve all existing Entrotter
and Colosseum work, PRs, evidence, media, history and branch protections. This
brief creates a separate Tokyo priority; it does not replace CODEX_GOAL.md's
longer-term Colosseum mission or authorize bulk integration of its open PRs.

Official submission deadline: **2026-09-27 09:00 JST / 2026-09-27 00:00 UTC**.
Use **08:00 JST** as an internal handoff target, not an official deadline.
Check the actual clock and current announcements before choosing scope. Do not
add features at the expense of an honest, reproducible submission package.

Final competition submission, registration-track changes, external video uploads,
feedback-form submission and outreach remain owner actions unless separately
and explicitly authorized. Prepare their inputs; never invent confirmation.

## 2. Sources and eligibility gate

Primary sources checked on September 26:

- Event rules, deadline and submission route:
  https://ethglobal.com/events/tokyo2026/info/start
- Detailed submission instructions:
  https://ethglobal.com/events/tokyo2026/info/details
- Tokyo Uniswap prize:
  https://ethglobal.com/events/tokyo2026/prizes/uniswap-foundation

The start page permits public libraries/boilerplate in Classic but excludes
pre-existing project-specific code, designs and assets. Continuity permits
existing code with new event-period functionality. The deadline is September 27
at 09:00 JST, with submission through the Hacker Dashboard. Confirm the actual
hacking start time rather than assuming September 25 at midnight.

The detailed instructions could not be retrieved during this audit. Read them
or the authenticated Dashboard when available; do not invent video limits,
required fields, exact AI-disclosure rules, sponsor-selection limits or judging
slots from earlier conversations or another event's requirements.

**A new repository, a new commit date, a license or an unmerged PR does not make
pre-event development new work.** Never redate, conceal or reset provenance.
Disclose the broader pre-existing Entrotter concept and product. A new independent
implementation still requires an honest eligibility assessment; do not claim
organizer approval without evidence.

## 3. Verified GitHub snapshot — distinguish main from candidates

The organization search returned six public repositories:

| Repository | Role |
| --- | --- |
| https://github.com/entrotter/entrotter | Coordination and evidence |
| https://github.com/entrotter/engine | Simulation/execution engine |
| https://github.com/entrotter/sdk-python | Python client |
| https://github.com/entrotter/cli | CLI |
| https://github.com/entrotter/scenarios | Scenarios and schemas |
| https://github.com/entrotter/entrotter.github.io | Static documentation/report viewer |

No Tokyo-specific repository or matching Tokyo issue was found in the searches
performed. This does not establish that no local or other-branch Tokyo work exists.
Inspect those before starting anything new.

### Main checkpoint

- Coordination main: `5401d56fdda7a33633e650439c2b33346a5ba835`.
- STATUS.md is dated September 20 and says **not submission-ready**.
- It records real Anvil execution, ERC-20 observation, archived Ethereum/Uniswap
  comparisons, and 121 Python plus 13 JavaScript tests at that checkpoint.
- Recorded example: Ethereum block 19,000,000; a successful WETH/USDC swap versus
  a minimum-output revert. These are archived-state action results, not proof of
  historical market replay, predicted prices or portfolio profitability.
- CODEX_GOAL.md targets Colosseum, not Tokyo.

Sources:
https://github.com/entrotter/entrotter/blob/5401d56fdda7a33633e650439c2b33346a5ba835/STATUS.md
https://github.com/entrotter/entrotter/blob/5401d56fdda7a33633e650439c2b33346a5ba835/CODEX_GOAL.md

### More advanced cumulative candidate — NOT merged

PR: https://github.com/entrotter/entrotter/pull/47

- Branch: `docs/reproducible-quick-start`.
- Head: `6eb5bc624d884e39efff9bc1444c6a6f590b14fa`.
- Open and unmerged when inspected; created and updated September 20.
- Contains recorded agent evaluations, bounded execution, reproducibility,
  security/dependency/link gates and recorded Colosseum submission materials.
- The candidate includes a 106.0675-second pitch with synthetic narration and a
  retained product demo. These are pre-event media, not Tokyo Classic deliverables.
- Its body identifies independent review, main integration and updated Pages
  deployment as outstanding. Do not describe candidate features as live on main.

The GitHub API returned completed/success for these exact-head workflow runs:

- Workspace integration:
  https://github.com/entrotter/entrotter/actions/runs/35486097390
- Coordination quality and dependency audit:
  https://github.com/entrotter/entrotter/actions/runs/35486097398
- Documentation links:
  https://github.com/entrotter/entrotter/actions/runs/35486097415

Cumulative component PRs linked by #47:

| Component | Candidate |
| --- | --- |
| Engine | https://github.com/entrotter/engine/pull/22 |
| SDK | https://github.com/entrotter/sdk-python/pull/6 |
| CLI | https://github.com/entrotter/cli/pull/9 |
| Scenarios | https://github.com/entrotter/scenarios/pull/8 |
| Viewer | https://github.com/entrotter/entrotter.github.io/pull/11 |

Engine #22's recorded head is
`2c843842dc57387150e3bb080c720bc94ce18bc5`. Re-read live heads, checks and reviews
before further work; references here are audit snapshots, not moving aliases.

Source inspection confirmed a Uniswap v3 ABI builder and ERC-20 observations:
https://github.com/entrotter/engine/blob/2c843842dc57387150e3bb080c720bc94ce18bc5/src/entrotter_engine/defi.py

The builder distinguishes legacy ISwapRouter from SwapRouter02. Existing model
and deterministic-policy results do not demonstrate a model advantage; direct
Anvil comparison does not establish a speed advantage. Preserve those findings.

The last recorded deployed viewer was the older main version at
`ab121348b0ffbec5650f9eadf0a0b11f639d9780`, run `35453228118`. A fresh live-site
check was unavailable in this audit. Latest-candidate deployment is unverified.

**Audit scope:** repository files, PR metadata and CI results were inspected.
Local runtime tests were not independently rerun. Test counts from different
checkpoints overlap and must not be added together.

## 4. P0 — establish honest provenance and choose the implementation

1. Read applicable AGENTS.md, CONTRIBUTING.md and SECURITY.md. Inspect dirty
   worktrees, active branches and existing Tokyo work. Preserve unrelated changes.
2. Record the official hacking window, exact refs, pre-existing work, new work,
   third-party dependencies and unresolved eligibility questions in PROVENANCE.md.
3. Continue a genuinely independent, event-period Tokyo implementation if one
   exists. Otherwise implement a small new prototype in a separate clean working
   directory/repository. Prefer `entrotter/tokyo2026` if available and remote
   creation is authorized. Check name collisions; do not overwrite anything.
   If publishing is blocked, preserve a separate local repository and report the
   exact missing permission rather than trying to bypass it.
4. Do not copy/import the old engine, SDK, CLI, schemas, report fixtures, frontend,
   artwork, videos or detailed project designs into the Classic candidate. Do
   not mechanically translate the old source into a new language to disguise
   reuse. Use general-purpose public dependencies and primary protocol documents,
   retain their licenses, and design the new Tokyo-specific implementation now.
5. Do not claim a certified clean-room process or guaranteed eligibility. Disclose
   the prior concept/product. Prepare an organizer question when interpretation
   remains unclear; leave its sending and any track change to the owner. Continue
   independent work that does not depend on that answer.
6. Only incorporate existing Entrotter code if the owner explicitly approves an
   appropriate track change and the relevant rules permit it. That is not the
   selected/default path for this task.

## 5. P1 — build one narrow Uniswap decision-checking demonstration

Proposed Tokyo scope: a small tool that compares alternative actions from the
same pinned onchain state and makes their consequences inspectable. Present it
as decision testing, not future prediction or reversal of production history.

Implement this vertical slice:

1. Accept a proposed swap and explicit user constraints.
2. Read a pinned chain state through a read-only upstream RPC. Create owned,
   isolated local Anvil states. Record chain ID, block number/hash, contracts,
   token decimals, tool versions, funding/impersonation overrides and assumptions.
3. Compare at least two meaningful alternatives from identical starting states.
   Include a real success and an adverse/revert/hold outcome. If adding a local
   price/liquidity disturbance, label it as engineered, apply the same exogenous
   sequence to both branches and do not call it an observed historical event.
4. Produce actual receipts, gas and exact native/ERC-20 balance changes plus an
   understandable proceed/reduce/hold explanation. Holding is an alternative
   action, not a reverted transaction. Compare under stated constraints, not an
   unsupported claim that one action is universally optimal.
5. Provide a small local script/CLI/API and a newly authored comparison UI.
   A deterministic policy is sufficient. Do not introduce an LLM for branding.
   If a model is actually used, retain its prompt/tool trace, causal observations,
   limits and available cost/seed details, and compare with a simple rule baseline.
6. Keep public hosting static. Publish the new report viewer to a separate GitHub
   Pages project path without replacing the existing root website. Label stored
   examples versus newly executed reports. Report import stays in the browser;
   GitHub Pages does not execute Python/Anvil. Do not fake a public Run button.

Uniswap v3 is a suitable initial target; do not force a last-minute v4/hook
rewrite. The published bounty accepts v2/v3/v4 and broader stack integrations.
It asks for public OSS code, FEEDBACK.md, a Developer Feedback Form submission
including that file's link, and README pointers to integration code/contracts.
Prepare evidence for these requirements; do not infer that integration alone
wins a prize. Avoid cosmetic extra-sponsor integrations.

Required form: https://developers.uniswap.org/hackathon-feedback

## 6. P1 — run tests and retain evidence

Run the new path end to end: clean setup, state pinning, branch creation, local
execution, report generation, import/render and the decision explanation.

Test success, revert/hold, identical initial conditions, wrong chain/block hash,
RPC failure, invalid amounts/decimals, malformed/tampered reports and process
cleanup. Report passed, failed and skipped tests separately; old tests are not
new Tokyo results. Pin source and dependencies and retain commands, environment,
logs and actual results from clean reproduction.

Never silently replace failed historical access with a synthetic fixture.
A separately labeled local mode is acceptable, but its provenance must remain
visible in the report, UI and demo.

Keep transaction writes on owned loopback nodes. No real keys, mainnet broadcasts,
public Anvil, arbitrary uploaded code, paid hosting or unapproved model spending.
Bound execution and clean up owned resources. Do not remove validation or tests
to produce a green badge. Do not promise production security or full sandboxing.

Token balance changes are not portfolio PnL. Do not add incompatible currencies,
claim prevented monetary losses without valuation assumptions, or invent an AI
or performance advantage. A report hash detects alteration, not model correctness.

Verify desktop/mobile rendering, keyboard use, error states and the published
site. Record deployment success AND an actual HTTP/browser check; a PR build is
not evidence that a new version is publicly deployed.

## 7. P2 — prepare Tokyo-specific submission materials

Create English deliverables inside the new Tokyo work, matching the actual
Dashboard fields once inspected:

| File / artifact | Required content |
| --- | --- |
| README.md | Problem, user, actual capabilities, architecture, tested quick start, exact integration source, demo distinction, provenance and limitations |
| SUBMISSION.md | Paste-ready title, short pitch, description, how made, challenges, accomplishments, event-period contributions, truthful links and prize justification |
| PROVENANCE.md | Pre-event concept/product, new implementation chronology, exact refs, dependencies/licenses and unknown eligibility issues |
| AI_USAGE.md | Actual tools, prompts/specifications, human contributions and known limits; no invented authorship claims |
| FEEDBACK.md | Genuine Uniswap integration feedback and the exact public link to include in the external feedback form |
| FEEDBACK_FORM_DRAFT.md | Prepared answers for the required form; distinguish prepared from actually submitted |
| DEMO_SCRIPT.md | Concise English walkthrough showing the real flow, one negative case and evidence |
| New recorded demo | The actual eligible-build recording, English captions and verified duration; not merely a script or old Colosseum footage |
| CHECKLIST.md | PASS / FAIL / BLOCKED / NOT APPLICABLE with evidence links and precise remaining owner actions |
| readiness.json | Small machine-readable copy of key gates and evidence pointers |

Use 90–120 seconds as an initial demo editing target, NOT as an asserted official
limit. Confirm the actual Tokyo cap. A repository MP4 is not automatically an
accepted hosted-video URL. Do not reuse pre-event clips, artwork or scripts as
new Classic media. Preserve the old Colosseum media unchanged.

Check registration/team facts, exact source/ref, demo URL, AI/prior-work
statements, sponsor conditions, feedback form, submission deadline and judging
requirements. Never guess personal fields. Do not copy Colosseum's video limits,
funding questions, school-status field or dates into Tokyo.

## 8. Execution loop and final handoff

Work in this order:

provenance audit -> smallest independent vertical slice -> real tests -> fixes ->
clear UI -> reproduction -> recording -> form-ready documents -> owner checklist.

Stop expanding scope once the core flow works. Do not rebuild all six components,
add unrelated sponsors or chase broad infrastructure goals before this deadline.
Do not bulk-merge PR #47 or its component candidates, bypass independent approval,
force-push, alter protections or conceal pre-existing work.

Where an external credential or approval blocks a step, continue independent
steps, save a checkpoint and state the smallest precise unblock action. Do not
repeatedly ask whether to continue. Do not claim indefinite background execution.

Return:

- Exact Tokyo repository and tested commit, or the local artifact and publication blocker.
- Verified demo/site URL, actual recorded video and any remaining hosting step.
- New test results, reproduction commands and evidence locations.
- Paste-ready English submission answers and sponsor requirement evidence.
- Candid eligibility status, including unresolved organizer questions.
- The smallest remaining owner actions before September 27 at 09:00 JST.

Completion means an evidence-backed, owner-reviewable package for genuinely
new event-period work. An old repository with a new README, a draft, an issue
comment, historical green CI or an unsupported submission claim is not completion.

