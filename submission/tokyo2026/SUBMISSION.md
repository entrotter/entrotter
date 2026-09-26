# English submission copy

## Project name
Entrotter Tokyo

## Category
Developer Tool

## Short description (under 100 characters)
Compare Uniswap actions from one pinned state with real receipts, gas and clear proceed/hold reasons.

## Description
A successful transaction can still be the wrong decision for a user's constraints. Entrotter Tokyo is
a small local tool for developers who want to inspect alternative Uniswap actions before giving an
onchain workflow execution permission. It compares a proposed swap, a smaller swap, an intentionally
strict minimum-output trial, and holding the position, each restored to the same pinned starting state.

The new Tokyo example executes real Uniswap v3 WETH/USDC swaps on a local Ethereum archive fork.
The proposed 0.2 WETH swap succeeds but exceeds a 0.1 WETH spending cap. The reduced swap receives
370.556838 USDC within the stated constraints. The strict-minimum trial actually reverts and spends
gas; holding executes nothing and costs zero execution gas. A static viewer exposes exact receipts,
raw balance accounting, assumptions and a client-only report import. It does not connect wallets or
run transactions on the public site.

This is a Continuity Track submission. The Entrotter concept and broader Colosseum implementation
existed before Tokyo. The separate CLI, comparison UI, tests and execution evidence submitted here
were newly authored during Tokyo; pre-event code, reports, artwork and video are not claimed as new.
Codex authored/assisted the implementation and documents under the owner's product specification,
scope, constraints and decisions. Full attribution and limits are in AI_USAGE.md and PROVENANCE.md.
This is decision testing, not historical replay, a market forecast, a profit claim or an AI trading agent.

## How it's made
The new implementation uses Python's standard library and pinned Foundry 1.8.3. An allowlisted
read-only RPC proxy supplies Ethereum block 23,000,000 to an owned loopback Anvil. The runner verifies
the chain and block hash, deployed contracts and token decimals. It impersonates a disclosed test
address, funds it locally, wraps WETH and approves the exact input. Funding and approval receipts
are retained separately from trial gas. Each alternative restores the same snapshot and verifies
balances, nonce, allowance, pool slot0 and liquidity. Explicit timestamps remove setup timing drift.

The integration uses Uniswap v3's deployed SwapRouter and factory, encoding exactInputSingle with
the correct legacy router tuple. It collects real receipts, gas costs and exact WETH/USDC/ETH changes.
A deterministic policy checks the user's spending, output and gas limits. The browser validates the
report hash, accounting, receipt gas and calldata before rendering it with plain HTML/CSS/JavaScript.
There are no runtime Python packages or model calls. The upstream transport rejects transaction writes.
Tests cover malformed data, wrong pins and actual Anvil cleanup after success, exception and SIGTERM.
This is an experimental bounded local tool, not a complete security sandbox.

## Challenges and accomplishments
We found that Anvil reports an uncomputed local state root and that automatic setup timestamps can
make receipts differ across reruns. We disclose the former and verify snapshot restoration using
explicit state observations; we fixed the latter with pinned timestamps. A fresh source extraction
then reproduced exact receipts, calldata and deltas. We retained the adverse result that the smaller
swap used slightly more gas. The value is inspectable evidence and constraint-aware comparison,
not a claimed speed, profit or model advantage.

## Uniswap prize integration
Actual v3 SwapRouter integration, a four-way decision-testing tool for the Uniswap ecosystem, public
MIT project code, source pointers and genuine FEEDBACK.md. The user-selected track is Continuity;
apply to the Continuity-specific Uniswap Stack Contribution prize, not the Classic prize pool.

## Links
- Source: https://github.com/entrotter/engine/tree/feat/tokyo-continuity/tokyo
- Viewer: https://entrotter.github.io/tokyo2026/
- Evidence: https://github.com/entrotter/entrotter/tree/docs/tokyo-continuity/evidence/tokyo2026
- Feedback: https://github.com/entrotter/entrotter/blob/docs/tokyo-continuity/submission/tokyo2026/FEEDBACK.md
- Video: see media/README.md; silent screen recording is supplemental, not a Finalist submission video.

Live/public status must be read from CHECKLIST.md and deployment evidence, not inferred from these URLs.
