// Benign control for top-level-require-method-call: the required module's own
// method is invoked at top level, so the trait must fire here.
const path = require("path");
path.join("a", "b");
