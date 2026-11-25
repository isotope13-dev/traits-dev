// Content script: click WhatsApp Web's send control for each recipient row.
const sendIcon = document.querySelector('span[data-icon="send"]');
// Popup: parse the imported CSV into rows.
function parseRows(csvData) { return csvData.split("\n").filter((line) => line.trim()); }
// Background: upload each recipient's number with its delivery status.
async function uploadReport(campaignState, userId) {
  const reportData = { userId, report: campaignState.report };
  await fetch("https://backend.example.test/report", { method: "POST", body: JSON.stringify(reportData) });
}
module.exports = { sendIcon, parseRows, uploadReport };
