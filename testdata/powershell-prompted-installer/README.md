# Operator-prompted installers are not poll-eval agents

`http-poll-eval-agent-loop` fires on loop + sleep + fetch + eval proximity.
A retry wrapper plus an interactive prompt loop plus a one-shot `IRM | IEX`
bootstrap (the shape of a documented installer such as Csound's
`getcsound.ps1`, which bootstraps the official Astral uv installer) matches
all four legs without being an agent: the loop never runs fetched code.

`micro-behaviors/os/console/io::operator-prompted-fetch-loop` (exception)
withholds the hostile when the loop prompts the operator (`Read-Host`);
`micro-behaviors/os/console/io::read-host-call` marks the operator read.

Run `python3 testdata/powershell-prompted-installer/check.py
<scratch-directory>`:

- `agent-loop-positive.ps1`: tight retrieve-eval-sleep loop. Must report
  the hostile.
- `prompted-installer-negative.ps1`: retry backoff, `while ($true)`
  `Read-Host` prompt loop, one-shot fetch-eval. Must report no hostile;
  the exception fires (verified with `cleave test-rules`) and the
  `read-host-call` notable surfaces.
