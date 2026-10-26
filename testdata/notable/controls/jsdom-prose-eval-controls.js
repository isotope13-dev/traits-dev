// Docs mention the option in prose (backticked) while unrelated code calls
// eval: the JSDOM sandbox is never configured here, so the composite that
// pairs the two must stay silent.
const { JSDOM } = require("jsdom");

// Pass `runScripts: "dangerously"` to enable in-page scripts, or
// `runScripts: "outside-only"` to expose window.eval instead.
function titleOf(window) {
  return eval(window.document.title);
}

module.exports = { titleOf };
