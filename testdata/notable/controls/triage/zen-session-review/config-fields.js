// These are configuration properties, with no serialized HTTP body.
const options = { apiKey: apiKey };
const DEFAULT_SESSION_MAX_AGE_MS = 30 * 60 * 1000;
const authPath = join(homedir(), ".pi", "agent", "auth.json");
