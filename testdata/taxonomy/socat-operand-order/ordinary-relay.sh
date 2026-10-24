#!/bin/sh
socat STDIO,raw,echo=0 TCP:192.0.2.10:9001
