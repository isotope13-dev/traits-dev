#!/bin/bash
set -euo pipefail
chmod -R 755 "/Applications/InternalTool.app"
codesign --verify --deep --strict "/Applications/InternalTool.app"
open -a "/Applications/InternalTool.app"
