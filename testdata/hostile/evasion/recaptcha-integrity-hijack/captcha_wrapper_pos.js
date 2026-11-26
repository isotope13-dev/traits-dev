// Page-world helper: wraps the reCAPTCHA Enterprise verifier and keeps the wrapper after load.
(function () {
  const key = Symbol.for("helper.captcha.v1");
  function wrap(fn) { return fn.toString().includes("extension_hijack_detected") ? false : true; }
  Object.defineProperty(globalThis, "grecaptcha", { configurable: true, set(v) { this._g = v; } });
  if (wrap(globalThis.grecaptcha && globalThis.grecaptcha.enterprise && globalThis.grecaptcha.enterprise.execute)) {
    globalThis[key] = "ready";
  }
})();
