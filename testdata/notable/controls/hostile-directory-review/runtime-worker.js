const fullPath = Deno.execPath();
Deno.run({ cmd: [fullPath, "run", "--allow-run", "worker.js"] });
