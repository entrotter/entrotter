# Entrotter Tokyo — compare before you commit

A successful swap is not necessarily an acceptable decision. This **Continuity Track** prototype
helps a developer inspect four alternatives from the same pinned Ethereum state before authorizing
an onchain action. It runs transactions only on an owned local Anvil fork and displays receipts,
exact token changes, gas and deterministic explanations against explicit user constraints.

[Report viewer](https://entrotter.github.io/tokyo2026/) · [Submission](SUBMISSION.md) ·
[Provenance](PROVENANCE.md) · [AI usage](AI_USAGE.md) · [Readiness](CHECKLIST.md) ·
[Uniswap feedback](FEEDBACK.md)

## Measured example

Ethereum block **23,000,000**, hash
`0xe368c631c74a82c3043e6d44c4bef6e6139a6501b39c7700c2552554d10e6c3b`.
Spend cap 0.1 WETH, minimum 2,000 USDC/WETH, execution gas cap 200,000.

| Alternative | Actual outcome | USDC change | Gas units | Decision |
|---|---|---:|---:|---|
| Swap 0.2 WETH | Success | +741.110419 | 130,800 | Hold: spending cap exceeded |
| Swap 0.1 WETH | Success | +370.556838 | 131,738 | Proceed under stated constraints |
| 0.2 WETH with excessive minimum | Revert | 0 | 140,461 | Hold: minimum-output failure |
| Hold | No transaction | 0 | 0 | Preserve balances |

Gas and ETH fees are reported separately. The smaller trade actually used slightly **more gas**;
we retain that result. These are new local execution results, not old Entrotter fixtures, historical
transaction replay, financial advice, price forecasts or a profit calculation.

## Reproduce

Prerequisites: Python 3.11+ on macOS/Linux and **Foundry 1.8.3** (`anvil` and `cast` on PATH).
No Python runtime packages, wallet, account or API key are required for the public endpoint used here.
Use the [official Foundry release](https://github.com/foundry-rs/foundry/releases/tag/v1.8.3), verify
its release checksums, then check `anvil --version` and `cast --version`. Network and archive availability
are prerequisites; installing Foundry is not included in the measured 14.04-second execution time.

```bash
git clone --branch feat/tokyo-continuity https://github.com/entrotter/engine.git
cd engine/tokyo
python3 compare.py --block 23000000 \
  --block-hash 0xe368c631c74a82c3043e6d44c4bef6e6139a6501b39c7700c2552554d10e6c3b \
  --amount 0.2 --max-spend 0.1 --min-rate 2000 --max-gas 200000 --output report.json
# In the existing website checkout on feat/tokyo-continuity:
# python3 -m http.server 8766 --bind 127.0.0.1 --directory tokyo2026
```

Open `http://127.0.0.1:8766` and import `report.json`. The public viewer is static and also imports
reports entirely in-browser. Its example is a **stored recording**, not a fresh remote run.
`TOKYO_RPC_URL` optionally selects an HTTPS archive endpoint; do not commit it. On macOS, if your
Python installation cannot find system certificates, use `SSL_CERT_FILE=/etc/ssl/cert.pem`.
Do not disable TLS verification. Failed archive access is an error, with no synthetic fallback.

## Tests and evidence

```bash
python3 -m unittest discover -s tests -v
# In the website checkout: node --test tests/tokyo-report.test.mjs
python3 tests/integration.py --anvil /absolute/path/to/anvil --cast /absolute/path/to/cast
```

8 Python tests and 16 JavaScript tests passed. The opt-in integration ran on an archive-backed
Anvil, passing five checks: exact fresh-run reproduction, successful cleanup, wrong hash rejection,
injected-exception cleanup and SIGTERM cleanup. It must be invoked separately: CI does not claim
archive coverage. [Integration evidence](../../evidence/tokyo2026/integration.json), [unit log](../../evidence/tokyo2026/unit-tests.log),
[report validation log](../../evidence/tokyo2026/report-tests.log), [measured report](../../evidence/tokyo2026/verified-run.json).
The fresh reproduction extracted source commit `50a73e7` into an independent temporary directory.
Browser evidence and recording status are tracked in [CHECKLIST.md](CHECKLIST.md).

## Architecture and exact Uniswap integration

`compare.py`: amount validation → source pin → allowlisted read proxy → owned Anvil → deposit/approve →
snapshot → four serial alternatives → receipts/balances → deterministic decision → hashed JSON.
`site/report.mjs` independently checks digest, initial observations, receipt gas, calldata amounts,
balance arithmetic and verdict consistency. `site/app.mjs` renders safely with text nodes.

The integration calls the actual Ethereum Uniswap v3 **SwapRouter**, not a mocked swap contract.
- Router: `0xE592427A0AEce92De3Edee1F18E0157C05861564`
- Factory: `0x1F98431c8aD98523631AE4a59f267346ea31F984`
- WETH: `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` (18 decimals)
- USDC: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` (6 decimals)
- Fee tier: 3,000; pool obtained by `getPool` and retained in each report.
- [Integration code](https://github.com/entrotter/engine/tree/feat/tokyo-continuity/tokyo/compare.py): `run()` calls `getPool`, verifies `decimals`, funds/approves WETH,
  encodes `exactInputSingle`, submits only on loopback and reads actual receipts.
- [Official address source](https://developers.uniswap.org/docs/protocols/v3/deployments/v3-ethereum-deployments).
- [Pinned official ABI source](https://github.com/Uniswap/v3-periphery/blob/764903fe5c8e274dc107163347cc2404ca0fd584/contracts/interfaces/ISwapRouter.sol).

## Limits and provenance

Artificial 100 ETH local funding, impersonation and WETH wrapping are explicit overrides. Setup gas
is retained separately. Branches reset the same owned snapshot and verify balances, nonce, allowance,
pool slot0 and liquidity; Anvil's local block stateRoot is zero/uncomputed, **not a Merkle proof**.
The upstream source state root is retained. No later historical transactions are replayed.
SHA-256 detects content changes; a party can recompute it, so it is not authenticity or economic proof.
There is no LLM policy, market model, arbitrary code execution or claim of production-grade isolation.
Anvil has CPU/time/file-descriptor/file-size bounds and cleanup; RSS is not kernel-capped on macOS.

The Entrotter concept and broader Colosseum product predate Tokyo. This event-period implementation,
viewer, evidence and recording were authored during this session. None of the six existing repositories
or PRs was merged or changed. [PROVENANCE.md](PROVENANCE.md) and [AI_USAGE.md](AI_USAGE.md) disclose
prior work, the owner-authorized track change, AI authorship and unresolved eligibility limits.

MIT for new code. Public dependencies/tools retain their own licenses; see [THIRD_PARTY.md](THIRD_PARTY.md).
