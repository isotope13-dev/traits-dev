// Environment setup: copy ANTHROPIC_API_KEY from the console.
// Register the new key, then delete old key only after deployments are updated.
const env = process.env.ANTHROPIC_API_KEY;
module.exports = { env };
