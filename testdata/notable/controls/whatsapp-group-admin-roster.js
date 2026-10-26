// Group-admin roster with no chat-platform backdoor relationship: the same
// adminIds push/includes vocabulary that a platform backdoor rule must not
// fire on without platform evidence (a platform library import or a
// platform API call). The long numeric literal is a newsletter JID, not a
// platform snowflake ID.
const adminIds = [];
const NEWSLETTER_JID = "120363422340494910@newsletter";
async function syncGroupAdmins(participants) {
  for (const participant of participants) {
    if (participant.admin === "admin" || participant.admin === "superadmin") {
      adminIds.push(participant.id);
    }
  }
  return adminIds;
}
function isGroupAdmin(id) {
  return adminIds.includes(id);
}
module.exports = { syncGroupAdmins, isGroupAdmin, NEWSLETTER_JID };
