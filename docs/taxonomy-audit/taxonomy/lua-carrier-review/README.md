# Lua carrier review

The legacy runtime file used identifier text and a byte pattern to claim Lua carrier and implant behavior. Identifier names do not establish that those operations occurred, and the byte pattern alone does not establish a carrier.

- Propagation and implant names are components under `metadata/lang/source/naming/propagation` and `metadata/lang/source/naming/implant`; the firewall-check name belongs under `metadata/lang/source/naming/action/security`.
- The raw record pattern belongs under `metadata/binary/section/bytes`.
- The combined Lua, service and name-or-record profile belongs under `metadata/file/profile/module-interop`; the propagation, implant and runtime-or-record profile belongs under `metadata/file/profile/operation-reference`. Their descriptions state the actual evidence rather than asserting a carrier.
- Eight distinctive name patterns now require one occurrence rather than three. Eight less distinctive name patterns retain their existing minimum of three. The name observations are components, and the aggregate profiles still require additional evidence. This intentionally broadens matching of the distinctive components.
- The unsupported technique annotation was removed. All other matching conditions and composite relationships were retained.
