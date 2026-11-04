#!/bin/sh
node -e 'require("child_process").spawnSync("bun", ["install", "bad-pkg"])'
