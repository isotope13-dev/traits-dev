var c = ["install", "--omit=dev", "--no-audit", "--no-fund", "--package-lock=false"];
if (ready) { c.push("--no-save", "--install-links"); }
runNpm(c, { cwd: projectRoot, timeout: 1800000 });
