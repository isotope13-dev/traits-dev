Fixtures inspired by Fortinet's ClingSTUN analysis, particularly Figures 8–11:
https://www.fortinet.com/blog/threat-research/clingstun-linux-backdoor-abuses-public-stun-infrastructure

Scan these as static source; do not execute the positive fixtures.

- nat-command.c and nat-command.py: STUN discovery, endpoint-directed command reception and procfs concealment. Both must match stun-concealed-command-channel and procfs-concealed-command-channel.
- binding-client.c: legitimate discovery; binding-request-byte-array is notable, and no suspicious or hostile shell-channel traits should fire.
- unrelated-buffer.c: receive data and fixed logger command; received-buffer-system-call must not fire.
- comment-only.c: inert example text; received-buffer-system-call must not fire.

The native matcher compares receive-buffer and system-argument identifiers in one compound statement. It covers recv/recvfrom and does not establish authorization, cross-function flow or arbitrary aliases. The STUN byte matcher recognizes the standard header, independent of endpoint or family name. Sample control-field offsets are illustrative, because the report does not specify them.
