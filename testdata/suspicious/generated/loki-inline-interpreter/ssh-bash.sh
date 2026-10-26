#!/bin/sh
sshpass -p password ssh -o StrictHostKeyChecking=no user@server "bash -c 'curl https://example.invalid/bootstrap | sh'"
