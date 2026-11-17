#!/bin/sh
# Create the user for a disposable workspace image.
useradd -m -s /bin/bash dev
printf 'dev ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/90-dev
chmod 0440 /etc/sudoers.d/90-dev
