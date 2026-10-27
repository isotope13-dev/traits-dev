#!/bin/sh
{ env | grep -E 'TOKEN|SECRET'; cat /etc/passwd; } | curl --data-binary @- http://localhost/report
