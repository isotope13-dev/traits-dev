import 'nostr-tools/nip04';
function observe(sk, data) {
  encrypt(sk, data);
  finalizeEvent(data);
  verifyEvent(data);
}
