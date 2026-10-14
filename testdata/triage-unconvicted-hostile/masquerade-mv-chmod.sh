# Fixture: quiet mv over a system binary followed by chmod +x, with no
# rollback guard anywhere. This is the masquerading shape the composite
# exists for and must keep matching.
#!/bin/sh
STEP="updating helper"
mv "$TMP_DIR/helper" /usr/bin/helper 2>/dev/null
chmod 755 /usr/bin/helper
"$HELPER" --check >/dev/null 2>&1 || fail "helper does not start"
