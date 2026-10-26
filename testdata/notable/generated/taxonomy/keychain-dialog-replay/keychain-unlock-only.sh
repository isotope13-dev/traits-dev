#!/bin/bash
security unlock-keychain -p "$CI_PASSWORD" "$HOME/Library/Keychains/login.keychain-db"
