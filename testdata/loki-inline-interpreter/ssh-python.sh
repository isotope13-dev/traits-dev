#!/bin/sh
sshpass -p password ssh -o StrictHostKeyChecking=no user@server "python -c 'import os; os.system(\"id\")'"
