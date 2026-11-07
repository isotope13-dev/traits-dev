#!/bin/bash
# Near miss: Finder quick action prints where each selected file came from and
# its campaign tag; no download, persistence, or device identifier.
for f in "$@"; do
  url=$(mdls -raw -name kMDItemWhereFroms "$f" | tr -d '()"\n ' | cut -d, -f1)
  tag=$(echo "$url" | sed -e 's/.*subid=\([[:alnum:]]*\).*/\1/')
  osascript -e "display notification \"$url ($tag)\" with title \"$(basename "$f")\""
done
