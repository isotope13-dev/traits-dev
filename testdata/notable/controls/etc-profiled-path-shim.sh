#!/bin/sh
# Static test case; do not execute this example.
# A benign installer PATH block: it mentions ssh sessions in a comment, writes
# a profile.d snippet, greps for its idempotency marker, and silences probes.
PROFILED="/etc/profile.d/example-shim.sh"
MARK_BEGIN="# >>> example-shim >>>"
MARK_END="# <<< example-shim <<<"
append_block() {
  grep -qF "$MARK_BEGIN" "$1" 2>/dev/null && return 1
  printf '%s\n' "$MARK_BEGIN" >> "$1"
  printf 'export PATH="/opt/example/bin:$PATH"\n' >> "$1"
  printf '%s\n' "$MARK_END" >> "$1"
}
install_profiled() {
  # ssh sessions source /etc/profile.d, so this also reaches remote logins.
  existing=$(cat "$PROFILED" 2>/dev/null | grep -v "^#" || true)
  if [ -w /etc/profile.d ] 2>/dev/null || [ "$(id -u)" = "0" ]; then
    append_block "$PROFILED" || true
  fi
  grep -qF "$MARK_BEGIN" "$HOME/.profile" 2>/dev/null || append_block "$HOME/.profile"
}
install_profiled
