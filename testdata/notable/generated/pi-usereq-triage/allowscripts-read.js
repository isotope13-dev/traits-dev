// Reads the policy to report pending approvals; never assigns it.
function pendingApprovals(pkg) {
  const map = pkg.allowScripts ?? {};
  return Object.entries(map).filter(([, v]) => v === true).map(([k]) => k);
}

module.exports = { pendingApprovals };
