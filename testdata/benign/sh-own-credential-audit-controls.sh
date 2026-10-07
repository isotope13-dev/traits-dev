set -u
# Administrator auditing their OWN credential files: single-user paths, no
# cross-user sweep, no live validation. Nothing harvested, nothing probed.

if [ -f "$HOME/.claude/.credentials.json" ]; then
  echo "claude credentials present"
fi
if [ -f "$HOME/.aws/credentials" ]; then
  echo "aws credentials present"
fi
