function version() { return JSON.parse(readFileSync('package.json')).version; }
// Windows npm .cmd shims need an interpreter.
function exec(name, args) { return spawnSync(name, args); }
