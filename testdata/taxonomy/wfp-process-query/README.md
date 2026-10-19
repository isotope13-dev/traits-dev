# WFP application identity and process path controls

The source fixtures distinguish parsed application-ID calls and process member
reads from declarations, comments, and quoted examples. These ordinary queries
must not imply security-product targeting or outbound blocking. The existing
`dotnet-self-copy-startup-binding/mainmodule-distinct.cs` control also retains
coverage after moving the member observation from `info/selfpath` to
`info/query`. The only exact YAML consumer was updated; no directory selectors
of either leaf required changes. The matcher now requires a parsed member
instead of unqualified text, independently of the placement correction.

The reviewed source samples are EDRSilencer technique reconstructions. Both
enumerate processes, select SentinelAgent.exe or CylanceSvc.exe, resolve their
paths to application IDs, and attempt to add blocking ALE_AUTH_CONNECT filters
for IPv4 and IPv6. They do not terminate those processes, install drivers,
escalate privileges, or set persistent-filter flags. The C++ helper checks the
first filter-add result before adding the second. The C# version ignores both
results and leaves `displayData.name` null: it should fail filter validation,
not successfully silence the agents as supplied. Intentional attempts to
disable protection support the malicious judgments; successful execution was
not observed. The hostile source descriptions therefore say "attempts".

References:

- [EDRSilencer upstream](https://github.com/netero1010/EDRSilencer)
- [FWPM_FILTER0 requirements](https://learn.microsoft.com/en-us/windows/win32/api/fwpmtypes/ns-fwpmtypes-fwpm_filter0)

The packed ELF reviewed alongside these sources is Prometei v4.42V_Unix64.
Analysis used a copy: restore the four-byte UPX PackHeader magic at 0x6d8cc,
remove the JSON overlay beginning at 0x6d8f0, then decompress with UPX. The
original sample was unchanged. Its runtime loader remains executable despite
the damaged recovery footer; the footer repair enables the analysis tool.

Recovered execution evidence:

- At 0x41ab10, the bot constructs its authenticated HTTP polling URL from its
  controller, ID, and key; 0x41ab3d calls the HTTP receive routine.
- The `exec` branch at 0x422a61 passes its argument to 0x4157f8, which creates
  a worker at 0x4157c8. That worker calls the statically linked `system` wrapper
  at 0x4413c0 with the supplied argument. The handler sends an `OK` reply.
- The `start_mining` branch at 0x421ebc calls the miner setup at 0x423231.
- The remote command surface also implements file transfer, deletion, and
  host-information commands. These are corroborating payload observations,
  not claims derived merely from UPX or entropy.

The ordered config/id/enckey plus parent-relay schema is a family fingerprint.
Its duplicate generic botnet objective was removed and `linux-bot` now carries
the hostile family identity. The packed subtype retains its loader-layout
requirement. No generic identity/key/relay combination is newly classified as
botnet behavior, and the config fingerprint no longer claims an HTTP technique.

Scratch controls changed all IDs, key material, IP, and relay hostname and
retained both hostile family findings. Removing the parent-relay fields removed
both family findings while preserving the packing observations. These controls
use the original ELF carrier; no binary specimen is stored in this fixture set.

- [Prometei configuration analysis](https://kohi.re/posts/prometei_crypto/)
- [Prometei Linux behavior analysis](https://cujo.com/blog/iot-malware-journals-prometei-linux/)
