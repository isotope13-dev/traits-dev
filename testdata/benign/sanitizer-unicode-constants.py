"""Block-boundary constants for an invisible-unicode sanitizer allowlist: bare
references to the Tags block and the Variation Selectors Supplement, with no
data being encoded, must not read as a smuggling encoder."""

TAG_BLOCK_BASE = 0xE0000
TAG_BLOCK_END = 0xE007F
VARIATION_SUPPLEMENT_BASE = 0xE0100

FIRST_TAG = chr(0xE0000)
LAST_TAG = chr(0xE007F)


def in_tag_block(codepoint):
    return TAG_BLOCK_BASE <= codepoint <= TAG_BLOCK_END
