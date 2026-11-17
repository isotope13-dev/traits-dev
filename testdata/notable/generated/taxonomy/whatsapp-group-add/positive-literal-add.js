// Invites one fixed participant with a literal add action.
export const inviteUser = (sock, jid, user) => sock.groupParticipantsUpdate(jid, [user], 'add');
