// Benign control: host package-manager prefixes are not container app
// roots. Must NOT fire absolute-app-source-root-path.
export function backgroundPath(userHome) {
  return [
    `${userHome}/.local/bin`,
    "/opt/homebrew/bin",
    "/opt/local/bin",
    "/usr/local/bin",
    "/usr/bin",
  ].join(":");
}
