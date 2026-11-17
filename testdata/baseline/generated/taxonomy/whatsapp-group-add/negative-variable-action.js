// The membership action is chosen by the caller at runtime, not a literal add.
export const applyMembership = (sock, jid, users, action) => sock.groupParticipantsUpdate(jid, users, action);
