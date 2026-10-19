#!/bin/sh
usermod -aG runtime alice && sudo chmod 2775 /workspace
usermod -G users sudo
usermod -G sudo-tools alice
usermod -G wheelhouse bob
