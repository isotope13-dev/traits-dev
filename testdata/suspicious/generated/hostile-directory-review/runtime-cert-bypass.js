const fullPath = Deno.execPath();
Deno.run({
  cmd: [fullPath, "run", "--unsafely-ignore-certificate-errors", "--allow-run", "worker.js"],
  stdout: "null",
  stderr: "null",
});
