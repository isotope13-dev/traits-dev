#!/bin/sh
python3 -c "import os; os.system('{0} {1} {2}'.format('bun', 'install', 'bad-pkg'))"
