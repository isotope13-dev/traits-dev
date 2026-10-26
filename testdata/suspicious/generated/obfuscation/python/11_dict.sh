#!/bin/sh
python3 -c "import os; d={'cmd':'bun install bad-pkg'}; os.system(d['cmd'])"
