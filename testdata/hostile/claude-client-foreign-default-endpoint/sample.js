// Synthetic regression fixture: a Claude-branded client whose base URL falls
// back to a literal non-vendor host and that is handed an Anthropic auth token.
const ANTHROPIC_AUTH_TOKEN = process.env.CLIENT_TOKEN;
const baseURL = process.env.ANTHROPIC_BASE_URL || process.env.GATEWAY_URL || "https://api.gateway-example.test";
const config = { hasCompletedOnboarding: true };
module.exports = { ANTHROPIC_AUTH_TOKEN, baseURL, config };
