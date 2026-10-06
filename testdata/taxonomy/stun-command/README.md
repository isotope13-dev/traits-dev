Fixtures inspired by Fortinet's ClingSTUN analysis, particularly Figures 8–11:
https://www.fortinet.com/blog/threat-research/clingstun-linux-backdoor-abuses-public-stun-infrastructure

Scan these as static source; do not execute the positive fixtures.

- nat-command.c and nat-command.py: STUN discovery, endpoint-directed command reception and procfs concealment. Both must match stun-concealed-command-channel and procfs-concealed-command-channel.
- binding-client.c: legitimate discovery; binding-request-byte-array is notable, and no suspicious or hostile shell-channel traits should fire.
- unrelated-buffer.c: receive data and fixed logger command; received-buffer-system-call must not fire.
- comment-only.c: inert example text; received-buffer-system-call must not fire.

The native matcher compares receive-buffer and system-argument identifiers in one compound statement. It covers recv/recvfrom and does not establish authorization, cross-function flow or arbitrary aliases. The STUN byte matcher recognizes the standard header, independent of endpoint or family name. Sample control-field offsets are illustrative, because the report does not specify them.

Cling transaction-ID variants from Nozomi Networks Labs (Figure 13):
https://www.nozominetworks.com/blog/a-stunning-disguise-cling-malware-masquerades-as-google-

transaction-flood.py models the documented opcode/method/IPv4/port/duration
layout with three unused bytes skipped by `3x`, rather than returned by `3s`.
It must match stun-transaction-id-task-channel and zero-id-stun-task-requests.
Zero transaction bytes are constructed by repetition rather than bytes(12).
The target and server are documentation addresses; do not execute this sample.
transaction-comments.py and transaction-string.py must not match those two
objectives or the zero-ID and command-field call traits.
zero-binding-discovery.py intentionally uses a zero ID but performs no task
decoding; it must match zero-id-binding-repeated-byte without either objective.
The existing benign binding-client.py uses a random transaction ID and must
not match either objective.
