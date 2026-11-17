#!/bin/bash

SOURCE_ORG=""
TARGET_USER=""
GITHUB_TOKEN=""
PER_PAGE=100
TEMP_DIR=""
if [[ $# -lt 3 ]]; then
    exit 1
fi

SOURCE_ORG="$1"
TARGET_USER="$2"
GITHUB_TOKEN="$3"

if [[ -z "$SOURCE_ORG" || -z "$TARGET_USER" || -z "$GITHUB_TOKEN" ]]; then
    echo "All three arguments are required"
    exit 1
fi
TEMP_DIR="./temp$TARGET_USER"

mkdir -p "$TEMP_DIR"
TEMP_DIR=$(realpath "$TEMP_DIR")
github_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    local data="${3:-}"
    
    local curl_args=("-s" "-w" "%{http_code}" "-H" "Authorization: token $GITHUB_TOKEN" "-H" "Accept: application/vnd.github.v3+json")
    
    if [[ "$method" != "GET" ]]; then
        curl_args+=("-X" "$method")
    fi
    
    if [[ -n "$data" ]]; then
        curl_args+=("-H" "Content-Type: application/json" "-d" "$data")
    fi
    
    curl "${curl_args[@]}" "https://api.github.com$endpoint"
}

get_all_repos() {
    local org="$1"
    local page=1
    local all_slugs="[]"

    while true; do
        local response
        response=$(github_api "/orgs/$org/repos?type=private,internal&per_page=$PER_PAGE&page=$page")

        local http_code="${response: -3}"
        local body="${response%???}"

        if ! echo "$body" | jq empty 2>/dev/null; then
            return 1
        fi

        if ! echo "$body" | jq -e 'type == "array"' >/dev/null; then
            return 1
        fi

        local repos_count
        repos_count=$(echo "$body" | jq length)

        if [[ "$repos_count" -eq 0 ]]; then
            break
        fi

        local page_slugs
        page_slugs=$(echo "$body" | jq '[.[] | select(.archived == false) | .full_name]')

        all_slugs=$(echo "$all_slugs" "$page_slugs" | jq -s 'add')

        ((page++))
    done

    echo "$all_slugs"
}

create_repo() {
    local repo_name="$1"
    local repo_data
    repo_data=$(cat <<EOF
{
    "name": "$repo_name",
    "description": "Shai-Hulud Migration",
    "private": true,
    "has_issues": false,
    "has_projects": false,
    "has_wiki": false
}
EOF
    )
    
    local response
    response=$(github_api "/user/repos" "POST" "$repo_data")
    
    local http_code="${response: -3}"
    local body="${response%???}"
    
    if echo "$body" | jq -e '.name' >/dev/null 2>&1; then
        return 0
    else
        if [[ "$http_code" =~ ^4[0-9][0-9]$ ]] && echo "$body" | grep -qi "secondary rate"; then
            sleep 600
            
            # Retry the request
            response=$(github_api "/user/repos" "POST" "$repo_data")
            http_code="${response: -3}"
            body="${response%???}"
            
            if echo "$body" | jq -e '.name' >/dev/null 2>&1; then
                return 0
            fi
        fi
        return 1
    fi
}

make_repo_public() {
    local repo_name="$1"
    local repo_data
    repo_data=$(cat <<EOF
{
    "private": false
}
EOF
    )

    local response
    response=$(github_api "/repos/$TARGET_USER/$repo_name" "PATCH" "$repo_data")

    local http_code="${response: -3}"
    local body="${response%???}"

    if echo "$body" | jq -e '.private == false' >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

migrate_repo() {
    local source_clone_url="$1"
    local target_clone_url="$2"
    local migration_name="$3"
    local repo_dir="$TEMP_DIR"

    if ! git clone --mirror "$source_clone_url" "$repo_dir/$migration_name" 2>/dev/null; then
        return 1
    fi

    cd "$repo_dir/$migration_name"
    if ! git remote set-url origin "$target_clone_url" 2>/dev/null; then
        cd - >/dev/null
        return 1
    fi

    # Convert to a regular repo temporarily to make changes
    git config --unset core.bare
    git reset --hard

    # Remove .github/workflows directory if it exists and commit
    if [[ -d ".github/workflows" ]]; then
        rm -rf .github/workflows
        git add -A
        git commit -m "Remove GitHub workflows directory"
    fi

    # Convert back to bare repo for mirroring
    git config core.bare true
    rm -rf *

    if ! git push --mirror 2>/dev/null; then
        cd - >/dev/null
        return 1
    fi

    cd - >/dev/null

    rm -rf "$repo_dir/$migration_name"

    return 0
}

process_repositories() {
    local repos="$1"
    local total_repos
    total_repos=$(echo "$repos" | jq length)
    
    if [[ "$total_repos" -eq 0 ]]; then
        return 0
    fi
    local success_count=0
    local failure_count=0
    
    for i in $(seq 0 $((total_repos - 1))); do
        local repo
        repo=$(echo "$repos" | jq -r ".[$i]")
        
        local migration_name="${repo//\//-}-migration"
        
        local auth_source_url="https://$GITHUB_TOKEN@github.com/$repo.git"
        local auth_target_url="https://$GITHUB_TOKEN@github.com/$TARGET_USER/$migration_name.git"
        # Create target repository
        if create_repo "$migration_name"; then
            # Migrate the repository
            if migrate_repo "$auth_source_url" "$auth_target_url" "$migration_name"; then
                # Make the repository public after successful migration
                if make_repo_public "$migration_name"; then
                    ((success_count++))
                else
                    ((success_count++))
                fi
            else
                ((failure_count++))
            fi
        else
            ((failure_count++))
        fi
    done
    
    return $failure_count
}

main() {
    for tool in curl jq git; do
        if ! command -v "$tool" &> /dev/null; then
            exit 1
        fi
    done
    
    local repos
    if ! repos=$(get_all_repos "$SOURCE_ORG"); then
        exit 1
    fi

    # Process all repositories
    process_repositories "$repos"
}

# Run main function
main "$@"