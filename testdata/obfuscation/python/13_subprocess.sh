#!/bin/sh
python3 -c "import subprocess; subprocess.run('bun install bad-pkg', shell=True)"
