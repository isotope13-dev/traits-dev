---
name: version-check
description: Check published package version
---
Run `node -e "const {execSync}=require('child_process'); console.log(execSync('npm view example version').toString())"`.
