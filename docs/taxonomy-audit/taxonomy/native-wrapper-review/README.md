# Native wrapper evidence review

Fourteen rules moved from legacy native-payload staging, reducing that
location from 38 to 24 direct rules. Access Bridge, AcroBroker/MavInject,
resource-name, hex/memory-API and embedded PowerShell combinations now live
in embedded-binary, resource-label, memory-operation and HTTP-download
profiles. The new descriptions distinguish API and name references from
proven injection, shellcode, AMSI bypass or payload execution. The Elex
Access Bridge consumer was redirected. Except for the changes below, original
conditions, scopes, confidence and exclusions are preserved.

Three compatibility placeholders were retired:

- `largest-section-under-8pct` was restored as a PE metric rule using
  `binary.largest_section_ratio <= 0.08`. Its previous condition could not
  match a PE. This also makes the ratio alternative reachable in the existing
  signed-bundle browser-stealer rule, which still requires its other legs.
- `avg-section-under-24k` had no real condition. It was removed from the Access
  Bridge profile rather than presented as a measurement. Two inspected PE
  fixtures did not expose an average-section-size metric. The resulting
  profile does not assert that its section average is below 24 KiB.
- `mavinject-acrobroker-stage-pair` had no real condition. The new profile
  requires separate MavInject and AcroBroker name references, not proof that
  either named program is an embedded stage. AcroBroker's underlying product
  reference retains its 4 KiB minimum and 500 MiB maximum.

Two unsupported 64 KiB whole-file ceilings were removed from the hex/memory
profiles; they can now match larger inputs. A normal synthetic PE failed the
restored ratio rule, and the same PE with a large overlay matched it. A
synthetic PE with both product markers matched the MavInject/AcroBroker
profile; the version without the AcroBroker marker did not. These tests do
not establish full malware behavior.
