#!/bin/sh
sshpass -p password ssh -o StrictHostKeyChecking=no user@server id; python -c 'print(1)'
