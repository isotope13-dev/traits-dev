// Model endpoint used by the editor integration when no proxy is configured.
const COPILOT_BASE = 'https://api.individual.githubcopilot.com';

function modelUrl(path) {
  return `${COPILOT_BASE}${path}`;
}

module.exports = { modelUrl };
