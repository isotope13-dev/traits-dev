# Callback-access second review

The supplied C++ specimen is byte-identical to the write-first detection fixture.
It declares request encoding and security-module ownership as external harness
interfaces, provides no implementations, and has no entry point. Its code depicts
callback clearing, but cannot establish an operational driver request layout.

The old hostile driver-client rule required only service registration, startup,
a device handle and IOCTL use. Those are neutral capabilities. Its eight driver
reference atoms and client composites moved from objectives/evasion/anti-av/driver
to micro-behaviors/os/kernel/device, preserving matchers and type/platform scopes.
The client is notable and no longer carries escalation/evasion mappings.
Exact consumers in driver-stack and vulnerable-driver-dispatch were updated;
no ancestor directory selectors select the relocated rules.

The PDB/device callback-access composite moved to micro-behaviors/os/kernel/callback
as pdb-driver-callback-access (notable). The former callback-blinding composite is
pdb-callback-writable-driver-access in the same leaf (suspicious): its required
co-occurrence warrants investigation but does not bind a write to a callback slot.
Its unsupported blinding description and T1562.001 mapping were removed.
No comment or filename exempts executable attack behavior.

Controls: kernel-pdb-inspection.c and driver-ioctl-query.c have no suspicious or
hostile findings (scores 2 and 3). Both IOCTL-order reconstruction fixtures have
zero hostile and one suspicious finding (score 47). The unknown-driver static
reconstruction has zero hostile/suspicious findings (score 8). These three static
fixtures moved to testdata/benign; expectations retain the neutral capabilities
and explicitly forbid hostile findings. Existing leaves were reused.

The extension retains two hostile wallet-export traits (precision 5.3 and 6.8).
Reverse engineering traced imported and generated phrases through the import
helper to a JSON POST containing text and geolocation. The generic repeated getStorage
name matcher was removed from browser storage: an unqualified operation name
is not evidence of a browser storage proxy. Existing Ethereum RPC traits retain
the actual contract-state query capabilities. The browser command grouping no
longer uses this generic token.

The Python artifact writes a Microsoft 365 Evilginx phishlet. Its two hostile
traits retain precision 4.5 and 3.7; descriptions now assert configuration rather
than running network interception. Connection-password keys require a scalar
value; bare key: mapping fields no longer imply a connection-string secret.
