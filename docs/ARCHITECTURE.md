# Architecture and boundaries

The product is a backend/CLI/SDK tool. GitHub Pages is a documentation and
read-only artifact surface, not the product's compute layer.

```
Local user or trusted agent developer
    CLI --> SDK --HTTP(loopback)--> Engine API
     |                              |
     +------ optional local import--+
                                    |
                         strict scenario validator
                             /             \
                   fixture model       Anvil adapter
                     offline        /                \
                              baseline Anvil     candidate Anvil
                                    \                /
                              versioned result artifact
                                       |
                         local inspection / static export
```

For archived-state mode, the operator provides an archive RPC via an environment
variable. Source reads are separate from local transaction execution. Anvil
itself also retrieves state from that provider. The workflow does not maintain a
full archival node, guarantee a provider's historical coverage, or reproduce
external systems. It does not change any real blockchain history.

The two EVM branches share a source block, balances/overrides and slot timestamps.
They do not share a mutable process. This avoids baseline-to-candidate state
contamination. A future transaction-replay engine must explicitly resolve nonce,
ordering and state conflicts after an intervention; it cannot just keep calling
`evm_mine` and pretend later canonical blocks have been replayed.

Do not equate Entropy with physical time reversal: entropy/time travel is the
brand metaphor. This software simulates decisions; it is not a physical time
machine and does not overturn thermodynamics.

Future hosted execution needs a real queue, cancelable jobs, process/container
isolation, API auth, rate/cost quotas, egress policy, bounded storage and explicit
tenant isolation. `http.server` and a subprocess are not that solution.
