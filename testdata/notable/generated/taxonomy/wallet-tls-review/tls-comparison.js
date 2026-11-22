export function configureTls(verificationMode, options) {
  if (verificationMode === 'certificate') {
    options.rejectUnauthorized = true;
    options.checkServerIdentity = () => undefined;
  }
  return options;
}
