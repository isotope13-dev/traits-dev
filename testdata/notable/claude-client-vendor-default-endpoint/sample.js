// Synthetic near miss: the same client shape, but the fallback is the vendor
// origin. A user-chosen gateway is a router setting, not a foreign default.
const ANTHROPIC_AUTH_TOKEN = process.env.CLIENT_TOKEN;
const baseURL = process.env.ANTHROPIC_BASE_URL || "https://api.anthropic.com";
const config = { hasCompletedOnboarding: true };
module.exports = { ANTHROPIC_AUTH_TOKEN, baseURL, config };
