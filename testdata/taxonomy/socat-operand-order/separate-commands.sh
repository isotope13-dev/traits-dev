#!/bin/sh
socat EXEC:sh STDIO; printf 'TCP:192.0.2.10:9001\n'
socat EXEC:sh STDIO # TCP:192.0.2.10:9001
socat EXEC:sh STDIO
printf 'TCP:192.0.2.10:9001\n'
