#!/bin/bash
if [[ "${UID}" == 0 ]]; then
  blkdiscard -f /dev/sda
  blkdiscard -f /dev/nvme0n1
fi
