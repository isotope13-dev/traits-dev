#!/bin/sh
node -e 'require("child_process").execSync(["bun", "install", "bad-pkg"].join(" "))'
