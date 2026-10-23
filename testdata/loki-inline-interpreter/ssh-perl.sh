#!/bin/sh
sshpass -p password ssh -o StrictHostKeyChecking=no user@server "perl -e 'system(\"id\")'"
