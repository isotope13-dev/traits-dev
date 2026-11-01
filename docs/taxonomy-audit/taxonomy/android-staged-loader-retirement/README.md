# Android staged-loader retirement

The last 36 rules under `dropper/staged-loader` were moved to Android
configuration, class-name, binary-string, file-write, module-loading and
asset-profile subjects, or to the payload module-loading sink. No YAML rule or
live YAML reference remains in the legacy staged-loader namespace. The broad
hosts-file ancestor consumer retains explicit references to the moved rules.

The module-loading sink was split by the indicated payload source: network,
embedded, transformed, or input of unknown origin. Its largest leaf contains
42 rules. A raw copy-and-register-jump pattern moved to instruction metadata;
the admitted executable-memory chain moved to `memory-branch`, which does not
assume a module loader or file launch. A GCM/API co-occurrence moved to a
profile because it does not establish module activation.

Android manifest strings, class-name clusters and unbound native API evidence
now describe their observations. Twelve severity levels were reduced where
those observations did not support the legacy finding. Inherited payload
technique tags were removed from generic facts, and a media-asset profile keeps
only the supported extension-masquerade mapping. The original match conditions
and their non-technique defaults were compared across all 91 reviewed rules.

The compact-DEX socket profile retains its existing four-megabyte limit because
its API combination also occurs in legitimate apps. That bound can miss larger
samples; improving it requires stronger distinguishing evidence or a corpus
review, not an assumption that the file size proves intent.
