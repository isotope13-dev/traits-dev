# CLR and resource staging review

The `%InjectionPersist%` configuration token and COMPLUS environment names
moved to their keyword and environment-reference subjects. The combination of
reflection-loader, token and host-name clues moved to a suspicious PE profile:
those references do not themselves establish persistence or injection. The
CLR metadata/overlay/decryptor-name combination moved to an overlay profile;
its API names and layout do not prove that the overlay was decrypted or run.
The Strictor-style resource and section/API combination moved to a suspicious
PE profile; its matches do not establish encrypted resource staging. Its
conditions are also used by a known Strictor profile, but that profile has a
separate 5 MB maximum, so this unbounded observation is not redundant.

The CLR IL-only/missing-metadata trait no longer suppresses matches by the
`efi/testdata` path. It is also used by two other anti-static findings; the
change applies to them as well. A path-based exception could hide the same
bytes at an attacker-chosen location. In a synthetic PE made from a managed
fixture, changing the metadata pointer and BSJB marker caused the analyzer to
omit `pe.clr.is_il_only`; the anomaly did not match at either neutral or
fixture paths. The unmodified managed fixture emits that metric. Thus the
positive malformed-file detection and the practical effect of removing the
path suppression remain unverified for that synthetic sample.

The legacy Pack-v3 staged rule was redundant: its only additional leg is
already required by its parent, and both have the same platform, file type,
severity and confidence. It had no external references. The parent and five
supporting format/packer rules moved intact from the 81-rule runtime directory
to `objectives/anti-static/pack/custom`, leaving 75 runtime rules and six custom
rules. There were no cross-directory local references. An empty legacy YAML
file was removed.

Other original conditions, scopes, confidence and exclusions were preserved;
the two local CLR configuration references were redirected. Names, severity
and unsupported attack annotations were adjusted to match the evidence.
