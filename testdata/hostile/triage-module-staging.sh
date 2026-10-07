#!/bin/sh
modprobe esp4
sysctl -w kernel.unprivileged_userns_clone=1
