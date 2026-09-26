# Owner instructions and scope history

The owner requested that Codex read `ENTROTTER_ETHGLOBAL_TOKYO_2026_CODEX_GOAL.md` from their
connected Google Drive and execute implementation, tests, fixes, demo recording, English submission
copy and a checklist. Inspect current workspaces and provenance first. Preserve Colosseum PR #47
and related PRs, media and evidence. Never present unmeasured results or undeployed demos as complete.

Initial track instruction: retain Start from Scratch, no copying pre-event Entrotter artifacts.
Scope: compare multiple Uniswap actions from identical onchain starting state, real receipts, gas,
balance changes and explicit execute/hold explanations. Missing access must be documented.

Subsequent explicit owner changes (same session, September 26):
1. "Continuity Trackでお願いします" — use Continuity Track.
2. "全て許可するので自動で実行して" — authorize necessary actions automatically, including
   publication, uploads and submission within the task. Do not invent facts or bypass platform rules.
3. "デモ動画も自動で撮ることを許可します" — explicitly authorize automated demo recording.

The implementation had already started independently when Continuity was authorized. We retained
that work instead of importing the pre-event product. The human owner set the purpose, narrow scope,
provenance boundaries and track. The implementation and documents were AI-assisted/AI-authored.
No claim is made that the owner manually authored the generated code or recorded narration.

## Implementation specification authored in this session
- One Python standard-library CLI, Foundry 1.8.3, Ethereum block 23,000,000 and its exact hash.
- An allowlisted read proxy between archive RPC and a process-owned loopback Anvil.
- Deposit and approve local WETH with disclosed funding and impersonation; same snapshot for each trial.
- Compare proposed amount, reduced amount, engineered excessive minimum output, and no transaction.
- Derive decisions from user input cap, minimum rate and gas limit; retain adverse outcomes.
- Validate report hash, exact arithmetic, receipts, action calldata and observed starting-state fingerprint.
- A newly authored static HTML/CSS/JavaScript viewer with client-only import and a local-command builder.
- New unit, actual archive reproduction and browser checks; recording from this UI only.
- Separate project Pages path; original six repositories unchanged.

4. Owner then required existing repositories to be updated instead of using a new Tokyo repository, and explicitly ordered deletion of both the temporary GitHub repository and local folder. Work and media must be migrated first.
