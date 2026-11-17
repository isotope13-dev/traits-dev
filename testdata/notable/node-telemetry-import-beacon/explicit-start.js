const https = require('https');

function startTelemetry() {
  const data = JSON.stringify({
    node_id: 'agent-' + Math.random().toString(36).slice(2),
    telemetry_type: 'm2m_init_handshake',
    timestamp: Date.now()
  });
  const req = https.request({ hostname: 'gateway.example.net', method: 'POST' });
  req.write(data);
  req.end();
}

module.exports = { startTelemetry };
