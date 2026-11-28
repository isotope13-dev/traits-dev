// Builds the npm arguments for one known release of a CLI, installed into a
// folder of its own. The version is fixed in the source, so nothing floats.
export function pinnedInstallArgs(dir) {
  return ["install", "--prefix", dir, "example-cli@1.4.2"];
}
