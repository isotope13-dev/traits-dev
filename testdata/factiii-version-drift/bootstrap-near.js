const load = await io.run("launchctl", ["bootstrap", domain, file]);
if (load.code !== 0) return failed(lines, "launchctl bootstrap", load.output);
