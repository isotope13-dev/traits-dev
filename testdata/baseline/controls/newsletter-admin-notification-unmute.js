export const unmuteNewsletterAdminActivity = (jid) =>
  newsletterUserSetting(jid, 'ADMIN_NOTIFICATIONS', false)
