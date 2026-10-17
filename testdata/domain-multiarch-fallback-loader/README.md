# Domain-held multi-arch fallback loaders

The raw-IP-gated dropper composites miss loaders whose staging host is a
variable holding a domain (dynamic DNS): `dk.sh` (apex4/Mirai-style loader)
fires the domain-aware pair

- `objectives/command-and-control/botnet/iot::domain-multiarch-protocol-dropper`
  (variable host, multi-client fallback, arch matrix, raw-socket channel,
  local exec), and
- `objectives/command-and-control/dropper/file-exec/command/shell::multiarch-protocol-literal-exec`
  (fallback clients, arch matrix, chmod 777, local exec).

Run `python3 testdata/domain-multiarch-fallback-loader/check.py
<scratch-directory>`:

- `loader-positive.sh`: sanitized loader on a documentation domain
  (inert). Must report both hostiles plus the relocated neutral
  `dev-tcp-variable-port-80` notable, and must never reference the removed
  `mirror-tcp-probe` id.
- `installer-negative.sh`: per-arch release installer (one HTTP client,
  `chmod +x`, foreground launch, no raw socket). Must report neither
  hostile.
