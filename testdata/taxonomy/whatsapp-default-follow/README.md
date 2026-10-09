# Default WhatsApp channel follow controls

The sinitech 1.2.1 archive (SHA256
`d80382320ed611131b7b9bafb003465c6d6241553f42e773e4ec561209e3eb87`)
ships a populated `DEFAULT_AUTO_FOLLOW_CHANNELS`, assigns it to
`DEFAULT_CONNECTION_CONFIG.autoFollowChannels`, merges those defaults into
socket configuration, and follows each configured channel on session open.
Comments claim no default exists; executable assignments contradict them.
The package has two hostile findings (session manipulation and trojanized
Baileys library), with precision 7.1 and 6.8. A byte-preserving archive control
with only that default array emptied has zero hostile findings.

The standalone newsletter module accepts caller configuration and has no
hostile or suspicious findings. The message builder likewise has none.
AntiBan has one suspicious finding for zero-width content variation; its
webhooks use caller-supplied destinations and credential snapshots stay local.
GitHub's fetched behaviors bundle has no hostile or suspicious findings.

`cases.json` records five positive and near-miss source controls. They verify
that caller configuration and a nearby example JID cannot convict a follow,
while a literal follow target still matches. They also separate header names
from event names, URL routes from imports, contact collections from numeric
limits, and command dispatch from upload telemetry. All cases were checked
using `cleave --traits-dir . --json` and assertions over emitted IDs.

The invocation composite moved from the social objective to the messaging
capability leaf. ContentVariator and addZeroWidth atoms moved to Unicode
string capabilities; their suspicious consumer retains its exact references.
The sole automation-directory consumer already requires a retained cleanup
atom in that directory, so these moves do not alter its optional quorum.
A scoped libsignal alias remains visible through existing dependency-source
metadata; an alias plus Baileys identity does not establish a hostile swap.
