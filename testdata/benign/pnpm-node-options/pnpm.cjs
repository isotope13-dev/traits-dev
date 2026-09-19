// Minimal reproduction of pnpm's lifecycle environment handling
// (pnpm@: exec/lifecycle): configured node options and the Yarn PnP loader
// are propagated to lifecycle scripts via NODE_OPTIONS --require.
function makeNodeRequireOption(modulePath) {
  let { NODE_OPTIONS } = process.env;
  NODE_OPTIONS = `${NODE_OPTIONS ?? ""} --require=${modulePath}`.trim();
  return { NODE_OPTIONS };
}
function makeEnv(data, opts, env) {
  if (opts.nodeOptions)
    env.NODE_OPTIONS = opts.nodeOptions;
  return env;
}
module.exports = { makeNodeRequireOption, makeEnv };
