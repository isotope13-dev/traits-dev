// Pull every contact, then message each one with a paced loop.
async function runCampaign(template) {
  const contacts = await window.WPP.contact.list();
  for (const c of contacts) {
    await window.WPP.chat.sendTextMessage(c.id._serialized, template);
    await new Promise((r) => setTimeout(r, 2000 + 1500 * Math.random()));
  }
}
module.exports = { runCampaign };
