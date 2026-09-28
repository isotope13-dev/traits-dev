# PowerShell dropper atoms follow their capability

Four remaining atoms in the PowerShell `execute-download` leaf described
capability evidence rather than a completed download-and-execute chain. They
now live with their respective capability:

- A WebClient URL ending in `.js` saved to a `.exe` path is a specialized
  WebClient download observation under `communications/http/download/webclient`.
- A `msiexec` command targeting an MSI in ProgramData and the `/norestart`
  option are installer observations under `process/create/installer/msi`.
- A GitHub web-raw URL ending in `.msi` is a URL reference under
  `communications/http/url/github`.

The rules preserve their original Windows platform and `[powershell, batch,
pe]` file-type scope. Their existing exact consumers now reference the
capability IDs. The WebClient save-path observation drops the old inherited
`B0030` tag. The GitHub URL reference is notable rather than suspicious by
itself; the URL leaf supplies its general communication tags. MSI installer
observations use `T1218.007` instead of inheriting transfer/dropper tags. The
installer objectives remain hostile only when their additional transfer,
installer, or remote-access evidence is present.

The dated-MSI-name helper (`letters + MMDD + .msi`) was retired. It described a
filename shape rather than an installer capability, and it was a weak alternate
to the actual MSI package-verb evidence. The ProgramData MSI objective now
requires the package verb alongside its remote MSI URL and ProgramData target.
This avoids treating an arbitrary date-like name as evidence of installation;
the fixture suite shows no expected hostile verdict depended on the heuristic.
