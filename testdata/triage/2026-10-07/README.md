# First reasoned review, 2026-10-07

7970ff8bc3ec: MALICIOUS StormAttack Windows service/DLL installer, not
WannaCry. Rizin shows 0x401260 deleting and rewriting LanmanServer's
ServiceDLL with the System32 StormServer DLL path; 0x401150 allocates remote
memory, writes the DLL path, resolves LoadLibraryA and starts a remote
thread. The entry installer extracts a DLL resource and can install its
own automatic service. The resource region is largely zeroed in this capture;
no ransomware encryption or live flood implementation is established.
Two existing hostile composites match, with precision 10.2 and 7.2.
The service rule description now states the API/registry co-occurrence it
actually tests. Removed the duplicate metadata GetEnvironmentVariable
substring rule; the existing os/env/read API-name rule owns this behavior.
The metadata environment-vars composite was also removed: Environment class
references alone do not establish environment-variable access.

5e2f1d7c2472: BENIGN Gutcheck 0.5.1, MERLIN Windows diagnostics module.
OutlookAuth lists credential target names, filters Office SSPI targets and
reports stale authentication configuration; cmdkey does not disclose passwords.
NetworkDependency's Documents/Desktop pair is a folder-redirection comment,
not Axios malware identity or beacon reconnaissance. PublishedDefinitions uses
interactive Microsoft device authorization to read SharePoint check data;
TokenCache encrypts an opt-in remembered token using Windows user protection.
Elevation invokes UAC RunAs and transfers check definitions as data.
No covert data export or hostile execution was found.

27449c5af42e: BENIGN Gameograf Grand Theft Auto VI Collage Live Wallpaper
1.1.12 Chrome extension. Reviewed manifest and first-party scripts: new-tab
wallpaper/widgets, local notes/preferences, Chrome search.query, weather GETs,
periodic JSON message/shortcut GETs. Remote message text is inserted with DOM
textContent; sponsored messages receive an Ad badge and can be dismissed or
disabled. No cookie/history capture, covert upload or remote code execution.
No trait changes are needed for this extension; no suspicious/hostile YAML
findings. Vendored jQuery is embedded, not a fetched dependency finding.

Trait moves and coverage changes:
- All three PowerShell cmdkey rules move from credential-access/cli to the
  existing os/security/credential-manager leaf. Listing and parsing nonsecret
  target metadata is notable, not credential theft. Both HTTP theft consumers
  retain their source legs using the new IDs. Optional .exe fixes real commands.
- Axios folder-name proximity moves to fs/path/personal, with matcher/scope
  preserved, neutral description and notable severity. The old rule had no
  exact or ancestor consumers elsewhere in the loaded YAML tree; a folder pair
  is not family evidence. Its unrelated product exclusion was removed.
- Locale early-return atom moves to data/control-flow/return. Require a
  language-region tag to avoid treating an ordinary 'no' answer as a locale.
  The MUI objective retains its OS-language-query and proximity requirements.

Controls: credential-list.ps1 and folder-pair.ps1 should emit only neutral
notable observations; locale-return.ps1 matches the return atom, while
ordinary-return.ps1 does not. These use existing admitted leaves and introduce
no directory partitions. Neither neutral cmdkey composite nor folder atom has
an intent claim. Final atomscan scans confirmed two hostile StormAttack traits and zero
suspicious/hostile traits on both benign archives. All four controls passed.
make validate is the final required action.

Engine boundary: metadata/encoded-payload/url on StormAttack originates in
cleave's decoder, not YAML. Its evidence is the printf GUID format
{%08X-%04X-%04x-%02X...}; percent decoding mistakes printf widths for URL
escapes. YAML suppressors cannot remove this engine-generated observation.
The sample's ML ensemble probabilities are independent of these YAML fixes.
The supplied sandbox page and public project page could not be retrieved;
judgements above are based on the bytes, not unsupported external claims.
