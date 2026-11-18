#!/usr/bin/env bash
# A command-guard test suite keeps its refusal cases as data: quoted
# arguments and here-doc rows handed to the guard under test. None of these
# names runs; the guard is asked to refuse them.
set -eu
refusal_rows() {
  cat <<'ROWS'
bare HOME|command|2|block-unsafe-rm: refused=shared-root|rm -rf $HOME
python shared inline|command|0|-|python -c 's = "rm -rf $HOME"'
node heredoc|command|2|refused=shared-root|node <<"JS"\nconst s = 'rm -rf $HOME';\nJS
ruby process|recursive-rm|ruby|ruby -e 'system("rm -rf $HOME")'
ROWS
}
while IFS='|' read -r name kind code reason payload; do
  printf '%s\n' "$name" >/dev/null
done < <(refusal_rows)
while IFS='|' read -r agent pids prompt state note; do
  :
done <<ROWS
claude|1 claude|$(printf '\xe2\x9d\xaf\xc2\xa0')|working|a live turn under an idle session
codex|2 codex|$(printf '\xe2\x80\xba')|unjudged|nothing it could tell
ROWS
