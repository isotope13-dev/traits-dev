#!/bin/sh
set -eu
cd "$(dirname "$0")"
# Resource and assembly names deliberately differ from the triaged sample.
mcs -target:exe -out:optimizer-carrier.exe -resource:optimizer.ps1,controls.ps1 Carrier.cs
mcs -target:exe -out:removal-carrier.exe -resource:remove-exclusion.ps1,controls.ps1 Carrier.cs
