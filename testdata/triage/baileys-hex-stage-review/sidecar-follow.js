export const customConfig = { newsletterIds: ['120363123456789012@newsletter', '120363123456789013@newsletter'] };
export async function autoFollowChannels(sock) {
  for (const id of customConfig.newsletterIds) {
    try { await sock.newsletterFollow(id); } catch {}
  }
}
