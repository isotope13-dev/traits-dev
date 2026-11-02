#!/bin/sh
# Benign setup snippet: vendor download into ~/bin, armed, then run in the
# foreground with visible output. No detached or hidden launch.
curl -sSL https://github.com/example/tool/releases/download/v1/tool -o ~/bin/tool
chmod +x ~/bin/tool
~/bin/tool --help
