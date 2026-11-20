#!/bin/bash
# Shell init for local developer tools.
eval "$(/opt/homebrew/bin/brew shellenv)"
eval "$(pyenv init -)"
eval "$(ssh-agent -s)"
