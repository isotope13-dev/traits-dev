export function requestPermission(payload, wallet) {
  const args = JSON.parse(payload);
  return wallet.acquireCertificate({...args, privileged: false});
}
