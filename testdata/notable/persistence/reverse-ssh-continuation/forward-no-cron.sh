#!/bin/bash
# one-off forward from a laptop, no persistence
ssh -N -f -o ExitOnForwardFailure=yes \
  -R 2201:127.0.0.1:22 \
  admin@bastion.example.com
