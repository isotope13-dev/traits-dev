# Fixture: installer atomic-upgrade rollback guard beside its own launcher
# chmod. The guarded `mv ... 2>/dev/null` restores the previous version when
# an update was cut off mid-swap; it is upgrade hygiene, not masquerading.
# Must never match quiet-mv-chmod-executable (the chmod below targets the
# launcher, a different file than the guard moves).
STEP="writing $LAUNCHER"
{
  printf '#!/bin/sh\n'
  printf '# An upgrade cut off mid-swap leaves the previous version beside the runtime: put it back.\n'
  printf '[ -e %s ] || { [ -f %s ] && mv %s %s 2>/dev/null; }\n' "$PKG_DIR" "$RUNTIME/cli.prev/bin/tool.js" "$RUNTIME/cli.prev" "$PKG_DIR"
  printf 'exec %s "$@"\n' "$NODE"
} >"$TMP_DIR/launcher" || fail "could not write the command"
chmod 755 "$TMP_DIR/launcher"
if ! same "$TMP_DIR/launcher" "$LAUNCHER"; then
  mv -f "$TMP_DIR/launcher" "$LAUNCHER" || fail "could not write $LAUNCHER"
fi
