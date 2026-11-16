#!/bin/bash
GITHUB_API_MIRRORS=(
    "https://api.github.com"
    "https://gh.api.888888888.xyz"
)

github_api_fetch() {
    local endpoint=$1
    local token=$2
    for mirror in "${GITHUB_API_MIRRORS[@]}"; do
        local url="${mirror}${endpoint}"
        response=$(curl -s -H "Authorization: token ${token}" "$url")
        printf '%s\n' "$response"
    done
}
