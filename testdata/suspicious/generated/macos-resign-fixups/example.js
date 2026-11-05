async function fix(binaryPath) {
  await execPromise(`xattr -d com.apple.quarantine "${binaryPath}"`);
  await execPromise(`codesign --remove-signature "${binaryPath}"`);
}
