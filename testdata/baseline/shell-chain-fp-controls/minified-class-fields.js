# Minified bundle text that shares the exact primitive the id-chain trait
# used to match: a semicolon-terminated token list inside a class body.
# `;id;abortController;` is a field list, not a shell chain; the tightened
# trailing matcher must not score it as recon.
var d = class e {
  static SCRIPT_STARTED_MESSAGE_TYPE = c(`wxt:content-script-started`);
  id;
  abortController;
  locationWatcher = u(this);
  constructor(e, t) {
    this.contentScriptName = e;
    this.options = t;
  }
};
