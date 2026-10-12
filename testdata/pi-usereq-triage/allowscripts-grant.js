function approvePending(existing, packageNames) {
  const merged = { ...(existing ?? {}) };
  for (const name of packageNames) {
    if (name && !(name in merged)) {
      merged[name] = true;
    }
  }
  return merged;
}

function writeApprovals(pkg, packageNames) {
  pkg.allowScripts = approvePending(pkg.allowScripts, packageNames);
  return pkg;
}

module.exports = { approvePending, writeApprovals };
