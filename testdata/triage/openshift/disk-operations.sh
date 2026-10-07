#!/bin/bash
blkdiscard /dev/vdb
blkdiscard "$dev" 2>/dev/null
