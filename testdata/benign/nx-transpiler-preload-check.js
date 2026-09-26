// Transpiler preload guard: skip a redundant loader registration when this
// process was already started with a TypeScript transpiler preloaded, either
// directly in `process.execArgv` or through `NODE_OPTIONS`.
function isTranspilerPreloaded() {
  const PRELOAD_FLAGS = ['-r', '--require', '--import', '--loader'];
  const TRANSPILER_RE = /(?:ts-node|@?swc-node)/;
  const execArgv = process.execArgv ?? [];
  for (const arg of execArgv) {
    if (PRELOAD_FLAGS.includes(arg)) return true;
  }
  // Preloads passed via NODE_OPTIONS don't surface in execArgv.
  const nodeOptions = process.env.NODE_OPTIONS;
  if (nodeOptions && TRANSPILER_RE.test(nodeOptions)) return true;
  return false;
}
module.exports = { isTranspilerPreloaded };
