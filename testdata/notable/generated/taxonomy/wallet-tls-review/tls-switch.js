export function configureTls(config, options) {
  switch (config.verificationMode) {
    case 'full':
      options.rejectUnauthorized = true;
      break;
    case 'certificate':
      options.rejectUnauthorized = true;
      options.checkServerIdentity = () => undefined;
      break;
  }
  return options;
}
