// A terminating helper must not suppress a separate runaway function.
function walk(node) {
  if (!node) return;
  const parent = node.parent;
  walk(parent);
}
function flood() {
  window.open("https://example.org");
  flood();
}
