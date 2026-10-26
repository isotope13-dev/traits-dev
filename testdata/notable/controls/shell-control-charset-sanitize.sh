#!/bin/sh
# Log sanitizer: strip C0 control characters so JSONL lines stay valid. The
# bracket glob below enumerates a control-character set with ANSI-C octal
# escapes — sanitizing, not a packed payload (it spells no printable text).
json_escape() {
  s="$1"
  if [ "$s" != "${s%%*[$'\001'-$'\010\013\014\016'-$'\037']*}" ]; then
    s="$(printf '%s' "$s" | tr -d '\000-\010\013\014\016-\037')"
  fi
  printf '"%s"' "$s"
}
