#!/bin/bash
blkdiscard "$dev" 2>/dev/null || true
