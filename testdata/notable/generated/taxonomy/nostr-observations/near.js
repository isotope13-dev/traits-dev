import 'nostr-tools/nip04';
function observe(other, data) {
  encrypt(other, data);
  finalizeEvent(data);
}
