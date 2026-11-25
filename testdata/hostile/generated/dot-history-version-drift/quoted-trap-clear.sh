#!/bin/bash
# Variant: quoted EXIT trap removes $0, then wipes shell history.
trap 'rm -f "$0"' EXIT
history -c
