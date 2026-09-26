# New Tokyo screen walkthrough — English script

Target: about 2 minutes 15 seconds, native playback speed, at least 720p. Capture the new viewer and
new measured report only. The automatic recording is silent, with captions; it is supplemental,
not a compliant Finalist video. A human can read this script for a separate compliant recording.

0:00–0:18 — Entrotter Tokyo compares decisions before execution. A transaction can succeed and still
violate your rules. This is our new Continuity prototype; the broader Entrotter concept predates Tokyo.

0:18–0:38 — This stored example was actually executed on a local Anvil fork of Ethereum block
23 million. Every alternative starts from the same restored snapshot. The cap is one tenth of a WETH,
the minimum rate is two thousand USDC per WETH, and the gas limit is two hundred thousand units.

0:38–0:58 — The proposed two-tenths WETH swap succeeded, receiving 741.110419 USDC. It still exceeds
the user's spending cap, so the decision is hold. The reduced one-tenth WETH swap receives 370.556838
USDC within the constraints. It uses slightly more gas, and we preserve that measured tradeoff.

0:58–1:18 — The deliberately excessive minimum output reverts. No WETH or USDC moves, but 140,461
gas units are spent. Holding is different: no transaction, no token changes and no execution gas.
Open the evidence to inspect the exact balances and receipt rather than trusting a green label.

1:18–1:38 — The source block, contracts, funding overrides and separate setup receipts are visible.
This does not replay historical trades or predict future prices. Balances are not portfolio profit.
The hash checks integrity, not truth; initial observations and receipt arithmetic are also validated.

1:38–1:58 — To test another proposal, build a local command, run Python and Anvil on your own computer,
then import its report here. The public site is static. Imports stay in your browser. A malformed
report is rejected and previous results are cleared.

1:58–2:15 — Our fresh reproduction matches receipts and deltas. Tests include success, revert, wrong
pins and cleanup on interruption. This is AI-assisted developer tooling with explicit provenance,
not an autonomous trading recommendation. Inspect the source, assumptions and real evidence.
