// The variable/call argument is passed to the returned require, not eval.
function hash(text) { return text.charCodeAt(0) ^ text.charCodeAt(1); }
const plugin = eval("require")(pluginPath);
const persist = eval("require")(path.resolve(configPath));
