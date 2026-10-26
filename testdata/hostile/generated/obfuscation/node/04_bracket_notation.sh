#!/bin/sh
node -e 'global["require"]("child_process")["execSync"]("bun install bad-pkg")'
