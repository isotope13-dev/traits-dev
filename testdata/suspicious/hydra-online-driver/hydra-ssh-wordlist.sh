#!/bin/sh
# Offline test-box credential check driven by a wordlist.
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.0.2.7
