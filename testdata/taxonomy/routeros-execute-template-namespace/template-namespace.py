"""Benign control: dollar-namespace template variables.

The command-word span here is a template-namespace reference where every
variable carries a colon-suffixed namespace, not a RouterOS command taking a
bare variable.
"""

_CODE_PAYLOAD_PREFIXES = frozenset(
    "/target /execute /tdd /fix /fno:target /fno:execute /fno:tdd "
    "/fno:fix $fno:target $fno:execute $fno:tdd $fno:fix".split()
)
