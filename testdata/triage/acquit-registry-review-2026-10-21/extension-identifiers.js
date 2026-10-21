// Static scanner fixture. Never execute.
function BINARY_EXTENSIONS() { return ['.foo']; }
function isBinaryExtension(name) { return BINARY_EXTENSIONS().includes(name); }
