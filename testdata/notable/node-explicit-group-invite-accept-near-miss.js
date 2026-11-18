// Near-miss for the remote group-join composite: a caller-supplied invite code
// is accepted once on an explicit request. There is no remote list, no fetch
// of JSON, and no delayed timer, so the host application chose the group.
async function joinGroupFromInvite(sock, inviteCode) {
  if (!/^[A-Za-z0-9_-]{16,}$/.test(inviteCode)) {
    throw new Error('invalid invite code');
  }
  return sock.groupAcceptInvite(inviteCode);
}

module.exports = { joinGroupFromInvite };
