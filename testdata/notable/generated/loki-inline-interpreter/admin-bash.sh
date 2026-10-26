#!/bin/sh
sshpass -p password ssh -o StrictHostKeyChecking=no user@server "bash -c 'npm install'"
