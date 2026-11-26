#!/bin/sh
case "$1" in
  sh | */sh | -sh | bash | */bash | dash | */dash | zsh) echo shell ;;
esac
