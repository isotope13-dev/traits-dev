#!/usr/bin/env node
if (!process.argv[2]) {
  console.log("bun is not installed. Install it with: curl -fsSL https://bun.sh/install | bash");
  process.exit(1);
}
