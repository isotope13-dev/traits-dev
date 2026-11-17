export async function followWhenRequested(sock, jid) {
  if (jid.endsWith('@newsletter')) {
    return sock.newsletterFollow(jid);
  }
}
