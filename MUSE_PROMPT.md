The previous trait repair failed validation.
Repair the errors below. Keep the change scoped to these validation errors.

Validation output:
make: Entering directory '/srv/data/rectifier/traits-dev'
/data/rectifier/bin/cleave --traits-dir . validate
Error: Failed to load traits from .

Caused by:
    Unknown file types found in trait files:
      ./metadata/font/container/traits.yaml: Unknown file type: 'font' (trait 'font-body-is-text' in ./metadata/font/container/traits.yaml)
      ./metadata/font/container/traits.yaml: Unknown file type: 'font' (trait 'font-content-is-archive' in ./metadata/font/container/traits.yaml)
      ./metadata/font/container/traits.yaml: Unknown file type: 'font' (trait 'font-content-is-encrypted-blob' in ./metadata/font/container/traits.yaml)
      ./metadata/font/container/traits.yaml: Unknown file type: 'font' (trait 'font-content-is-executable' in ./metadata/font/container/traits.yaml)
      ./metadata/font/container/traits.yaml: Unknown file type: 'font' (trait 'font-header-size-disagrees' in ./metadata/font/container/traits.yaml)
      ./metadata/font/container/traits.yaml: Unknown file type: 'font' (trait 'font-leading-whitespace-padding' in ./metadata/font/container/traits.yaml)
      ./metadata/font/container/traits.yaml: Unknown file type: 'font' (trait 'font-no-signature' in ./metadata/font/container/traits.yaml)
      ./metadata/font/container/traits.yaml: Unknown file type: 'font' (trait 'font-signature-recognized' in ./metadata/font/container/traits.yaml)
      ./metadata/font/container/traits.yaml: Unknown file type: 'font' (trait 'font-structure-problem-reported' in ./metadata/font/container/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-interior-gap-bytes' in ./metadata/font/layout/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-overlapping-tables' in ./metadata/font/layout/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-oversized-private-table' in ./metadata/font/layout/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-stowaway-archive' in ./metadata/font/layout/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-stowaway-encoded' in ./metadata/font/layout/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-stowaway-executable' in ./metadata/font/layout/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-stowaway-high-entropy' in ./metadata/font/layout/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-stowaway-script' in ./metadata/font/layout/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-table-out-of-bounds' in ./metadata/font/layout/traits.yaml)
      ./metadata/font/layout/traits.yaml: Unknown file type: 'font' (trait 'font-trailing-data' in ./metadata/font/layout/traits.yaml)
      ./objectives/anti-static/obfuscation/payload/font/carrier.yaml: Unknown file type: 'font' (composite rule 'font-carries-opaque-stowaway' in ./objectives/anti-static/obfuscation/payload/font/carrier.yaml)
      ./objectives/anti-static/obfuscation/payload/font/carrier.yaml: Unknown file type: 'font' (composite rule 'font-carries-payload-behind-edited-directory' in ./objectives/anti-static/obfuscation/payload/font/carrier.yaml)
      ./objectives/anti-static/obfuscation/payload/font/carrier.yaml: Unknown file type: 'font' (composite rule 'font-carries-unclaimed-payload' in ./objectives/anti-static/obfuscation/payload/font/carrier.yaml)
      ./objectives/anti-static/obfuscation/payload/font/carrier.yaml: Unknown file type: 'font' (composite rule 'font-directory-hand-authored' in ./objectives/anti-static/obfuscation/payload/font/carrier.yaml)
      ./objectives/anti-static/obfuscation/payload/font/carrier.yaml: Unknown file type: 'font' (composite rule 'font-embeds-archive' in ./objectives/anti-static/obfuscation/payload/font/carrier.yaml)
      ./objectives/anti-static/obfuscation/payload/font/carrier.yaml: Unknown file type: 'font' (composite rule 'font-embeds-executable' in ./objectives/anti-static/obfuscation/payload/font/carrier.yaml)
      ./objectives/anti-static/obfuscation/payload/font/carrier.yaml: Unknown file type: 'font' (composite rule 'font-embeds-script' in ./objectives/anti-static/obfuscation/payload/font/carrier.yaml)
      ./objectives/evasion/masquerade/extension-mismatch/font.yaml: Unknown file type: 'font' (composite rule 'font-file-is-disguised-text' in ./objectives/evasion/masquerade/extension-mismatch/font.yaml)
      ./objectives/evasion/masquerade/extension-mismatch/font.yaml: Unknown file type: 'font' (composite rule 'font-file-is-padded-non-font' in ./objectives/evasion/masquerade/extension-mismatch/font.yaml)
      ./objectives/evasion/masquerade/extension-mismatch/font.yaml: Unknown file type: 'font' (composite rule 'font-named-file-is-archive-blob' in ./objectives/evasion/masquerade/extension-mismatch/font.yaml)
      ./objectives/evasion/masquerade/extension-mismatch/font.yaml: Unknown file type: 'font' (composite rule 'font-named-file-is-executable-blob' in ./objectives/evasion/masquerade/extension-mismatch/font.yaml)
      ./objectives/evasion/masquerade/extension-mismatch/font.yaml: Unknown file type: 'font' (composite rule 'font-named-file-is-opaque-blob' in ./objectives/evasion/masquerade/extension-mismatch/font.yaml)
    
    Update cleave or fix these 'for:' values.
make: *** [Makefile:21: validate] Error 1
make: Leaving directory '/srv/data/rectifier/traits-dev'


Before finishing, you MUST run:
  make -C /data/rectifier/traits-dev validate CLEAVE=/data/rectifier/bin/cleave

Fix every error and rerun until it passes.
