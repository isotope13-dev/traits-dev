// Benign control for top-level-require-method-call: the call on the line
// after require targets an unrelated object (console), not the require
// result, so the trait must stay silent here.
const routerDevtools = require("@tanstack/react-router-devtools");
console.warn("placeholder");
