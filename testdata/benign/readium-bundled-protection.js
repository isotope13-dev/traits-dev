// Bundled @readium/navigator protection module (esbuild module comment):
// node_modules/@readium/navigator/dist/protection/DevToolsDetector.js
// The opt-in detector times a constructor debugger call and reports
// open/closed to the host reader app through callbacks.
class DevToolsDetector {
  async checkDebuggerBased() {
    const start = performance.now();
    try {
      (() => {}).constructor("debugger")();
    } catch {
      debugger;
    }
    return performance.now() - start > 100;
  }
}
