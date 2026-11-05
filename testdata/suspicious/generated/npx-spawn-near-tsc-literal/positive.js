const args = ["tsc", "-p", "tsconfig.json", "--noEmit"];
spawn("npx", args, { shell: true });
