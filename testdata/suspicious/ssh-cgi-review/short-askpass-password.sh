#!/bin/sh
set -eu
target_host=$1
target_port=${2:-22}
acct=${3:-operator}
flag_path=$(mktemp -u)
ask_bin=$(mktemp)
cat >"$ask_bin" <<'HELPER'
#!/bin/sh
if test -f "$STATE_MARKER"; then
  head -c 32 /dev/zero | tr '\0' 'x'
  printf '\n'
else
  : >"$STATE_MARKER"
  printf 'init\n'
fi
HELPER
chmod +x "$ask_bin"
STATE_MARKER="$flag_path" SSH_ASKPASS="$ask_bin" SSH_ASKPASS_REQUIRE=force DISPLAY=:0 \
  ssh -F /dev/null -p "$target_port" \
  -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
  -o PreferredAuthentications=password -o NumberOfPasswordPrompts=2 \
  "$acct@$target_host" whoami </dev/null
rm -f "$flag_path" "$ask_bin"
