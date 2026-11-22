export function configureTls(verificationMode, options) {
  switch (verificationMode) {
    case 'full':
      options.rejectUnauthorized = true;
      break;
  }
  return options;
}

export function requestPermission(request, wallet) {
  switch (request.type) {
    case 'certificate':
      return wallet.acquireCertificate({privileged: true});
  }
}
