#!/bin/bash
# Disk wipe of the attached data volume
dd if=/dev/zero of=/dev/sda bs=1M
