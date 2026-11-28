function walk(dir) {
  if (!fs.existsSync(dir)) { return; }
  return fs.readdirSync(dir);
}
