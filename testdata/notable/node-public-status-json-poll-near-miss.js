// Near-miss for the attested remote-text feed poll: the same interval and
// fetch primitives, but the status endpoint is public, carries no Bearer
// token, and the request reports nothing about the host. The reply is parsed
// as JSON for a dashboard refresh, which is ordinary monitoring.
const STATUS_URL = 'https://status.example-vendor.com/api/v1/status';
let pollTimer = null;

async function refreshStatus(render) {
  const response = await fetch(STATUS_URL, { headers: { Accept: 'application/json' } });
  const status = await response.json();
  render(status.components);
}

function startStatusPoll(render) {
  refreshStatus(render);
  pollTimer = setInterval(() => refreshStatus(render), 60000);
}

module.exports = { startStatusPoll };
