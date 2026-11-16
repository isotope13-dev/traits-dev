#!/bin/bash
github_api_fetch() {
    local token=$1
    curl -s -H "Authorization: token ${token}" https://api.github.com/user
}
