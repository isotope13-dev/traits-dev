#!/bin/sh
path=".git/hooks/post-commit"
cat > "$path" <<'HOOK'
#!/bin/sh
git diff --patch HEAD^ HEAD > /tmp/patch.txt
HOOK
