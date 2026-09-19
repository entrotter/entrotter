# One default worker per Docker daemon

[Tracking issue](https://github.com/entrotter/entrotter/issues/24).
The proposed engine change builds on [bounded defaults](BOUNDED_DEFAULT.md).
It preserves the v0.1 scenario/result contract and is subject to independent
review. Frozen historical engine/scenario inputs remain unchanged.

Previously, two independent CLI or API processes each generated a new Docker
name and could simultaneously consume the full per-worker resource allowance.
The actual pre-fix regression shows both a successful extra CLI run and API 201
while another bounded worker occupied the daemon.

The new runner reserves the fixed `entrotter-active-worker` name. Docker's name
reservation arbitrates simultaneous creation; the preflight query is only a fast
rejection path. All matching default host runners on that daemon share one slot.
A preflight occupied-slot rejection fails the CLI without replacing its export
and returns API 429 `worker_busy_retry_later`. There is no queue or automatic POST retry. A simultaneous
creation conflict returns a generic execution failure (API 422): Docker can
reserve a name before its container appears in queries. The real race test
exposed that visibility gap. Failed starts are not misclassified as safe-to-retry
busy rejections; callers must not blindly retry a POST.

Each invocation adds an unpredictable owner label. Cleanup queries that owner
and removes only its validated full container ID. A late finalizer never removes
by the reused shared name, and a rejected caller does not delete the incumbent.
Failed daemon queries or uncertain cleanup fail explicitly.

The real-Docker suite synchronizes two separate Python processes immediately
after both observe an empty slot, then delays the real worker entrypoint by five
seconds. This timing fault injection retains actual Docker admission and kernel
controls; exactly one contender must finish the complete native-equivalent
fixture report. Other checks cover real engine CLI/API rejection and recovery,
a shortened host timeout, an unstarted container, and an independent idle worker
expiring on its actual 180-second timer. Protocol mocks are separately labelled.

The standalone CLI/SDK/API integration also holds a real idle worker, verifies
local CLI rejection, one API POST yielding 429, unchanged export and incumbent,
and successful execution after explicit release. Existing quota, connection
saturation, real Anvil receipts and recovery checks remain enabled.

## Boundaries

- This limits worker containers per configured daemon. It does not cap the number
  of Python callers, Docker/VM overhead, independent daemons or explicit native
  execution. Older runners use different names and do not share this admission.
- The 180-second timer begins in the worker entrypoint. A container abandoned
  before that entrypoint starts or a failed daemon may need operator inspection
  and removal by its exact ID. The regression confirms an unstarted container
  blocks capacity rather than being silently deleted.
- Host export retention, temporary files left by abrupt host death, image/build
  cache and VM storage still need separate limits. Fork workers retain bridge
  networking; arbitrary external agent code stays disabled.
- Source/image pins and full local/Linux results belong in
  `evidence/daemon-admission/summary.json`. No mixed-revision test is evidence for
  a final source pin. Tests do not establish a production multi-tenant service.
