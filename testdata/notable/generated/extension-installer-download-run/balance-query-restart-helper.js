// Near-miss regression fixture: a balance query and a local restart helper share
// a module. The fetch returns JSON that is never executed, and the spawn runs a
// fixed local service command, so no download-and-run flow exists here.
async function getBalance(accountId) {
  const res = await fetch(`https://api.example.com/accounts/${accountId}/balance`);
  return res.json();
}

// Unrelated helper section kept deliberately long so the two statements above
// and the restart helper below are far apart in the file. Nothing here fetches.
function formatCurrency(amount, currency) {
  const whole = Math.trunc(amount);
  const cents = Math.abs(Math.round((amount - whole) * 100));
  return `${currency} ${whole}.${String(cents).padStart(2, "0")}`;
}

function restartService() {
  const { execSync } = require("child_process");
  execSync("systemctl restart example-app.service");
}

module.exports = { getBalance, formatCurrency, restartService };
