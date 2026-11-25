// CRM reminder sender driven by the rows of a spreadsheet the user imported.
async function sendReminders(sheet, template) {
  for (let i = 0; i < sheet.rows.length; i++) {
    const row = sheet.rows[i] || [];
    await window.WPP.chat.sendTextMessage(row[0] + '@c.us', template);
    await new Promise((r) => setTimeout(r, 1000 + 1000 * Math.random()));
  }
}
module.exports = { sendReminders };
