// Reduced from Braintrust's module loader and independent CLI helpers.
// The names must not imply that these functions decode or execute a blob.
function runConsoleCall(callback) {
  return callback();
}
function runCatchFinally(f, catchF, finallyF) {
  try { return f(); } catch (error) { return catchF(error); }
  finally { finallyF(); }
}
function truncateToByteLimit(s, byteLimit = 65536) {
  return s.slice(0, byteLimit);
}
function executableSearchPath() {
  return process.env.PATH;
}
function serializeToolExecutionInput(args) {
  return args;
}
function traceToolExecution(args) {
  return args;
}
function loadModule({ inFile, moduleText }) {
  new Function("require", "module", "__filename", "__dirname", moduleText)(
    require, module, inFile, require("node:path").dirname(inFile)
  );
}
