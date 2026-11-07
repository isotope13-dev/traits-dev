#!/bin/sh
nc -l 4444
nc -lvnp 8080
nc -l 0.0.0.0 9000
netcat --listen 7000
