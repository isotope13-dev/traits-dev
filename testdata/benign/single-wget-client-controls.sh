#!/usr/bin/env bash
# Single-client BusyBox fetch (benign control): one `busybox wget` retrieval
# uses a single download client, so it must never count as multi-client
# download fallback even though both the bare-wget and BusyBox-wget atoms
# observe the same command.
set -e
busybox wget https://example.com/firmware/stable.bin -O /tmp/stable.bin
