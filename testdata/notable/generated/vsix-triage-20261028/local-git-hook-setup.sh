#!/bin/sh
hook_dir="$(git rev-parse --git-dir)/hooks"
mkdir -p "$hook_dir"
cat > "$hook_dir/post-commit" <<'HOOK'
#!/bin/sh
git diff --unified=0 HEAD^ HEAD > /tmp/local-commit-review.patch
HOOK
chmod +x "$hook_dir/post-commit"
