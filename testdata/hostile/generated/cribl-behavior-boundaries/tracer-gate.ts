if (process.env.LD_PRELOAD) { process.exit(0); }
const status = fs.readFileSync("/proc/self/status", "utf8");
