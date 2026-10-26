// Template-compiler directory walk (handlebars precompiler shape): `root`
// is the template root directory, not a credential, and `|| path` is a
// default-expression fallback, not a brute-force credential pair.
function enqueue(queue, path, root, extension, childPath) {
  if (extension.test(childPath)) {
    queue.push({ template: childPath, root: root || path });
  }
}

module.exports = { enqueue };
