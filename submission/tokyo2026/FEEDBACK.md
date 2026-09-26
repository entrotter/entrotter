# Uniswap developer feedback — Tokyo 2026

Integration: actual v3 SwapRouter `exactInputSingle` on a pinned Ethereum archive fork, WETH/USDC at
fee tier 3000. See [compare.py](https://github.com/entrotter/engine/tree/feat/tokyo-continuity/tokyo/compare.py), `run()` and `send()`, and [actual receipts](../../evidence/tokyo2026/verified-run.json).
No Uniswap API key, v4 hook, production transaction or partner endorsement is claimed.

What worked: published deployment addresses and the explicit single-hop parameter struct made it
possible to compare exact input/minimum-output choices with actual balance deltas. Reading token
decimals and the factory pool address before execution helped make the experiment auditable.

Friction observed in this session: the older ISwapRouter documentation URL redirected to a general
getting-started guide. A guessed version-tag source URL returned 404; a pinned official source commit
resolved it. Legacy SwapRouter includes a deadline in its tuple, unlike other router interfaces;
examples should make the router/address/ABI pairing prominent.

Requested improvement: one minimal versioned example that pins chain/block/router, approves the
exact input, demonstrates both success and minimum-output revert, and separates setup gas from swap
gas. A clear link from each deployment address to its exact interface would reduce integration errors.

Archive access had a User-Agent interoperability issue and Anvil setup timing needed explicit pins.
These are infrastructure/tooling findings, not claims of Uniswap contract bugs. No protocol security
vulnerability was identified by this narrow test.

Form link to include: https://github.com/entrotter/entrotter/blob/docs/tokyo-continuity/submission/tokyo2026/FEEDBACK.md
Feedback form status is in [CHECKLIST.md](CHECKLIST.md); a prepared file is not a submitted form.
